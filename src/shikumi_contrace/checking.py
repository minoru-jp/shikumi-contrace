"""Check contract assets (specification REG_003-REG_028, API_006, API_007).

Checks look at the runtime state after import (REG_002); they only report
(REG_006). The ranges of contract assets, tests and implementations are module
paths (REG_011).
"""

from __future__ import annotations

import ast
import dataclasses
import enum
import importlib
import inspect
import pkgutil
import sys
import types
import typing
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from shikumi_contrace._model import (
    DEPENDENCY,
    KIND,
    MEMBER,
    ON_VIOLATION,
    SUBJECT,
    attr_of,
    infos_on,
    iter_tests,
    namespace_of,
    parent_class,
    root_class,
)
from shikumi_contrace._structure import CONTRACT_ASSET_STRUCTURE, structure_findings
from shikumi_contrace._vocabulary import INV, POST, PRE, violates
from shikumi_contrace.reading import bindings_of, dependencies_of, relations_of

__all__ = ["CONTRACT_ASSET_STRUCTURE", "ContraceWarning", "Diagnostic", "check"]


class ContraceWarning(UserWarning):
    """The warning category the pytest integration reports diagnostics with."""


@dataclass(frozen=True)
class Diagnostic:
    """One finding of a check."""

    code: str
    message: str
    subject: str


def _origin(obj: object) -> str | None:
    if isinstance(obj, types.ModuleType):
        return obj.__name__
    if inspect.isclass(obj) or inspect.isroutine(obj):
        module_name = attr_of(obj, "__module__")
        return module_name if isinstance(module_name, str) else None
    return type(obj).__module__


def _qualified_name(obj: object) -> str:
    return f"{attr_of(obj, '__module__')}.{attr_of(obj, '__qualname__')}"


def _longest(roots: Iterable[str], name: str) -> int:
    best = -1
    for root in roots:
        if name == root or name.startswith(root + "."):
            best = max(best, len(root))
    return best


def _forbidden_role(
    origin: str | None,
    contract_assets: Iterable[str],
    tests: Iterable[str],
    implementations: Iterable[str],
) -> str | None:
    """The role of the longest matching range wins (REG_015)."""
    if not origin:
        return None
    contract = _longest(contract_assets, origin)
    tests_length = _longest(tests, origin)
    impl_length = _longest(implementations, origin)
    if max(tests_length, impl_length) > contract:
        return "tests" if tests_length >= impl_length else "implementations"
    return None


def _is_stdlib(module_name: str) -> bool:
    top = module_name.split(".")[0]
    return top == "builtins" or top in sys.stdlib_module_names


def _modules_under(root: str) -> Iterator[types.ModuleType]:
    module = importlib.import_module(root)
    yield module
    path = attr_of(module, "__path__")
    if path is not None:
        for info in pkgutil.walk_packages(cast("Iterable[str]", path), root + "."):
            yield importlib.import_module(info.name)


def _contract_closure(contract: type) -> Iterator[type]:
    """Yield *contract* and its valid direct/transitive dependencies once."""
    stack = [contract]
    seen: set[int] = set()
    while stack:
        current = stack.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        yield current
        valid = [
            dependency
            for dependency in dependencies_of(current)
            if infos_on(dependency, SUBJECT)
        ]
        stack.extend(reversed(valid))


# The module or package that holds the boundary types (IND_010).
PORTS = "ports"
_CONTRACE = "shikumi_contrace"


def _ports_root(origin: str | None) -> str | None:
    """The boundary-types module or package a module path belongs to, if any.

    ``pkg.ports.orders`` belongs to ``pkg.ports``; ``pkg.contracts`` belongs to
    none.
    """
    if not origin:
        return None
    parts = origin.split(".")
    if PORTS not in parts:
        return None
    return ".".join(parts[: parts.index(PORTS) + 1])


def _referenced_ports_root(origin: str | None, contract_module: str) -> str | None:
    """Return a referenced ``ports`` root only when it can belong to the asset.

    A third-party module such as ``vendor.ports.types`` is not boundary types of
    ``shop.contract.order`` merely because its import path contains ``ports``.
    For a qualified ``ports`` package, its parent must contain the contract
    module. A top-level ``ports`` remains a candidate so that the placement rule
    can report that invalid layout.
    """
    root = _ports_root(origin)
    if root is None:
        return None
    parent, separator, _ = root.rpartition(".")
    if not separator:
        return root
    if contract_module == parent or contract_module.startswith(parent + "."):
        return root
    return None


def _refers_to_contrace(origin: str | None) -> bool:
    return bool(origin) and (
        origin == _CONTRACE or str(origin).startswith(_CONTRACE + ".")
    )


def _ports_referenced_by(modules: Iterable[types.ModuleType]) -> set[str]:
    """The boundary-types modules that the contract modules refer to (REG_012)."""
    found: set[str] = set()
    for module in modules:
        if _ports_root(module.__name__):
            continue
        for name, value in namespace_of(module).items():
            if name.startswith("__") and name.endswith("__"):
                continue
            root = _referenced_ports_root(_origin(value), module.__name__)
            if root:
                found.add(root)
    return found


def _derive(
    test_modules: Sequence[types.ModuleType],
) -> tuple[set[str], set[str], set[str]]:
    """Derive the three ranges from what the tests declare (REG_012)."""
    contract_assets: set[str] = set()
    tests: set[str] = set()
    implementations: set[str] = set()
    for module in test_modules:
        for test in iter_tests([module]):
            relations = relations_of(test)
            if relations:
                tests.add(module.__name__)
            for relation in relations:
                contract = root_class(relation.clause)
                for asset in _contract_closure(contract):
                    contract_assets.add(asset.__module__)
            for binding in bindings_of(test):
                origin = _origin(binding.implementation)
                if origin and not _is_stdlib(origin):
                    implementations.add(origin)
    # The boundary types that the contracts refer to are part of the contract asset.
    contract_assets |= _ports_referenced_by(
        sys.modules[name] for name in sorted(contract_assets)
    )
    return contract_assets, tests, implementations


def _own_classes(module: types.ModuleType) -> Iterator[tuple[str, type]]:
    stack: list[tuple[str, type]] = [
        (f"{module.__name__}.{name}", value)
        for name, value in namespace_of(module).items()
        if isinstance(value, type) and value.__module__ == module.__name__
    ]
    while stack:
        path, cls = stack.pop()
        yield path, cls
        for name, value in namespace_of(cls).items():
            if (
                isinstance(value, type)
                and value.__qualname__ == f"{cls.__qualname__}.{name}"
            ):
                stack.append((f"{path}.{name}", value))


def _check_references(
    module: types.ModuleType,
    contract_assets: set[str],
    tests: set[str],
    implementations: set[str],
) -> Iterator[Diagnostic]:
    namespaces: list[tuple[str, dict[str, object]]] = [
        (module.__name__, namespace_of(module))
    ]
    namespaces += [(path, namespace_of(cls)) for path, cls in _own_classes(module)]
    reported: set[tuple[str, str]] = set()
    for path, namespace in namespaces:
        for name, value in namespace.items():
            if name.startswith("__") and name.endswith("__"):
                continue
            origin = _origin(value)
            role = _forbidden_role(origin, contract_assets, tests, implementations)
            key = (f"{path}.{name}", origin or "")
            if role and key not in reported:
                reported.add(key)
                yield Diagnostic(
                    "independence",
                    f"a contract asset refers to {role}: {path}.{name} -> {origin}",
                    f"{path}.{name}",
                )


def _refers_to_contract(origin: str | None, contract_names: set[str]) -> bool:
    if not origin:
        return False
    return any(
        origin == name or origin.startswith(name + ".") for name in contract_names
    )


def _is_data_type(cls: type[object]) -> bool:
    """Protocols and data: what the boundary types may define (IND_012)."""
    return (
        bool(attr_of(cls, "_is_protocol"))
        or dataclasses.is_dataclass(cls)
        or issubclass(cls, enum.Enum)
        or typing.is_typeddict(cls)
        or (tuple in cls.__mro__ and attr_of(cls, "_fields") is not None)
    )


def _check_ports(
    module: types.ModuleType, contract_names: set[str]
) -> Iterator[Diagnostic]:
    """The boundary types hold no contract and no behavior, and refer to no contract (REG_023, REG_024)."""
    name = module.__name__
    is_init = attr_of(module, "__path__") is not None and _ports_root(name) == name
    for path, cls in _own_classes(module):
        if infos_on(cls, SUBJECT):
            yield Diagnostic(
                "ports-contract",
                f"{path}: a contract does not belong in the boundary types ({PORTS})",
                path,
            )
    for attr, value in namespace_of(module).items():
        if attr.startswith("__") and attr.endswith("__"):
            continue
        origin = _origin(value)
        where = f"{name}.{attr}"
        defined_here = (
            inspect.isfunction(value) or isinstance(value, type)
        ) and attr_of(value, "__module__") == name
        if defined_here and is_init:
            yield Diagnostic(
                "ports-definition-in-init",
                f"{where}: the __init__ of {PORTS} holds no definitions; define it in a module of the package",
                where,
            )
        elif inspect.isfunction(value) and defined_here:
            yield Diagnostic(
                "ports-behavior",
                f"{where}: the boundary types hold no functions",
                where,
            )
        elif (
            isinstance(value, type)
            and defined_here
            and not _is_data_type(cast("type[object]", value))
        ):
            yield Diagnostic(
                "ports-behavior",
                f"{where}: the boundary types hold only Protocols and data, not {value.__name__}",
                where,
            )
        if _refers_to_contrace(origin) or _refers_to_contract(origin, contract_names):
            yield Diagnostic(
                "ports-reference",
                f"{where}: the boundary types refer to a contract or to shikumi-contrace ({origin})",
                where,
            )


def _imported_names(package: types.ModuleType) -> set[str]:
    """The absolute dotted names that the source of a package imports."""
    path = attr_of(package, "__file__")
    if not isinstance(path, str):
        return set()
    try:
        tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return set()
    names: set[str] = set()
    base_parts = package.__name__.split(".")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = ".".join(base_parts[: len(base_parts) - (node.level - 1)])
                module_name = f"{base}.{node.module}" if node.module else base
            else:
                module_name = node.module or ""
            names.add(module_name)
            names.update(f"{module_name}.{alias.name}" for alias in node.names)
    return names


def _check_ports_parents(
    module: types.ModuleType, contract_names: set[str]
) -> Iterator[Diagnostic]:
    """Importing the boundary types runs the ``__init__`` of its parents (REG_024)."""
    parts = module.__name__.split(".")
    for end in range(1, len(parts)):
        ancestor = ".".join(parts[:end])
        package = sys.modules.get(ancestor)
        if package is None:
            continue
        for imported in sorted(_imported_names(package)):
            if _refers_to_contrace(imported) or _refers_to_contract(
                imported, contract_names
            ):
                root = _ports_root(module.__name__) or module.__name__
                yield Diagnostic(
                    "ports-parent",
                    f"{ancestor}: its __init__ imports a contract or shikumi-contrace ({imported}); importing {root} would load it",
                    ancestor,
                )
                break


def _check_ports_placement(
    ports_root: str, tests: set[str], implementations: set[str]
) -> Iterator[Diagnostic]:
    """The package that holds ``ports`` is a contract asset, so it holds no test or implementation (REG_028)."""
    parent = ports_root.rpartition(".")[0]
    if not parent:
        yield Diagnostic(
            "ports-placement",
            f"{ports_root}: the boundary types are placed directly inside the package that holds the contracts, not at the top level",
            ports_root,
        )
        return
    for role, roots in (("a test", tests), ("an implementation", implementations)):
        for root in sorted(roots):
            if root == parent or root.startswith(parent + "."):
                yield Diagnostic(
                    "ports-placement",
                    f"{parent}: the package that holds {PORTS} contains {role} ({root}); tests and implementations are placed outside it",
                    parent,
                )
                break


def _check_ports_structure(ports_root: str) -> Iterator[Diagnostic]:
    """The structure of the package that holds ``ports``, checked with Shikumi (REG_027)."""
    parent = ports_root.rpartition(".")[0]
    if not parent:
        return
    for message in structure_findings(importlib.import_module(parent)):
        yield Diagnostic("ports-structure", f"{parent}: {message}", parent)


def _check_shapes(modules: Sequence[types.ModuleType]) -> Iterator[Diagnostic]:
    """A Protocol that is not the subject type of a contract belongs in the boundary types (REG_026)."""
    subjects: set[int] = set()
    for module in modules:
        for _path, cls in _own_classes(module):
            subjects.update(id(subject) for subject in infos_on(cls, SUBJECT))
    for module in modules:
        for attr, value in namespace_of(module).items():
            if (
                isinstance(value, type)
                and value.__module__ == module.__name__
                and "." not in value.__qualname__
                and bool(attr_of(value, "_is_protocol"))
                and id(value) not in subjects
            ):
                where = f"{module.__name__}.{attr}"
                yield Diagnostic(
                    "shape-outside-ports",
                    f"{where}: a Protocol that is not the subject type of a contract belongs in the boundary types ({PORTS})",
                    where,
                )


_POSITIONAL = {PRE: "member", POST: "member", INV: "subject"}


def _check_structure(module: types.ModuleType) -> Iterator[Diagnostic]:
    for path, cls in _own_classes(module):
        parent = parent_class(cls)
        kinds = infos_on(cls, KIND)
        violation_behaviors = infos_on(cls, ON_VIOLATION)
        # Read the parent's declarations once (mypy infers the type variable of
        # infos_on badly when the calls sit inside a conditional expression).
        parent_members: tuple[object, ...] = (
            infos_on(parent, MEMBER) if parent is not None else ()
        )
        parent_subjects: tuple[type, ...] = (
            infos_on(parent, SUBJECT) if parent is not None else ()
        )
        if kinds and parent is not None and kinds[0] in _POSITIONAL:
            needed = _POSITIONAL[kinds[0]]
            has = parent_members if needed == "member" else parent_subjects
            if not has:
                where = "a member" if needed == "member" else "a contract"
                yield Diagnostic(
                    "position",
                    f"{path}: the clause kind {kinds[0].name} belongs directly under {where}",
                    path,
                )
        if violation_behaviors and (not kinds or kinds[0] != PRE):
            yield Diagnostic(
                "violation-position",
                f"{path}: on_violation belongs to a PRE clause",
                path,
            )
        members = infos_on(cls, MEMBER)
        if members and parent_subjects:
            referred = attr_of(members[0], "__name__")
            if isinstance(referred, str) and referred != cls.__name__:
                yield Diagnostic(
                    "member-name",
                    f"{path}: the class name differs from the member it refers to ({referred})",
                    path,
                )

        dependencies = infos_on(cls, DEPENDENCY)
        subjects = infos_on(cls, SUBJECT)
        if dependencies and not subjects:
            yield Diagnostic(
                "dependency-position",
                f"{path}: depends_on belongs in a contract class",
                path,
            )
        for dependency in dependencies:
            if not infos_on(dependency, SUBJECT):
                yield Diagnostic(
                    "dependency-target",
                    f"{path}: depends_on refers to a class that is not a contract: {_qualified_name(dependency)}",
                    path,
                )


def _check_dependency_cycles(
    modules: Sequence[types.ModuleType],
) -> Iterator[Diagnostic]:
    roots: list[type] = []
    seen_roots: set[int] = set()
    for module in modules:
        for _path, cls in _own_classes(module):
            if infos_on(cls, SUBJECT) and id(cls) not in seen_roots:
                seen_roots.add(id(cls))
                roots.append(cls)

    state: dict[type, int] = {}
    stack: list[type] = []
    reported: set[frozenset[int]] = set()

    def visit(contract: type) -> Iterator[Diagnostic]:
        state[contract] = 1
        stack.append(contract)
        for dependency in dependencies_of(contract):
            if not infos_on(dependency, SUBJECT):
                continue
            dependency_state = state.get(dependency, 0)
            if dependency_state == 0:
                yield from visit(dependency)
            elif dependency_state == 1:
                start = stack.index(dependency)
                cycle = stack[start:] + [dependency]
                key = frozenset(id(item) for item in cycle[:-1])
                if key not in reported:
                    reported.add(key)
                    names = " -> ".join(_qualified_name(item) for item in cycle)
                    yield Diagnostic(
                        "dependency-cycle",
                        f"contract dependency cycle: {names}",
                        _qualified_name(dependency),
                    )
        _ = stack.pop()
        state[contract] = 2

    for root in roots:
        if state.get(root, 0) == 0:
            yield from visit(root)


def _check_tests(modules: Sequence[types.ModuleType]) -> Iterator[Diagnostic]:
    reported: set[tuple[int, int]] = set()
    for test in iter_tests(modules):
        name = _qualified_name(test)
        bindings = bindings_of(test)
        for relation in relations_of(test):
            contract = root_class(relation.clause)
            subjects = infos_on(contract, SUBJECT)
            if subjects and (id(test), id(contract)) not in reported:
                reported.add((id(test), id(contract)))
                if not bindings:
                    yield Diagnostic(
                        "unbound",
                        f"{name} relates to {contract.__qualname__} but has no binding",
                        name,
                    )
                elif not any(b.subject is subjects[0] for b in bindings):
                    yield Diagnostic(
                        "binding-mismatch",
                        f"{name} binds a different type than the subject of {contract.__qualname__}",
                        name,
                    )
            clause_kinds = infos_on(relation.clause, KIND)
            if (
                relation.word == violates.word
                and clause_kinds
                and clause_kinds[0] in (POST, INV)
            ):
                yield Diagnostic(
                    "unusual-combination",
                    f"{name}: violates is not usually used with {clause_kinds[0].name} clauses",
                    name,
                )


def check(
    *,
    contract_assets: Sequence[str] | None = None,
    tests: Sequence[str] | None = None,
    implementations: Sequence[str] | None = None,
    test_modules: Sequence[types.ModuleType] = (),
) -> list[Diagnostic]:
    """Check contract assets and return the findings; an empty list means none.

    The ranges are either *declared* (``contract_assets``, ``tests``,
    ``implementations``: module paths) or *derived* from what the modules in
    ``test_modules`` declare. If any of the three is given, nothing is derived
    and the roles not given are empty (REG_011, API_007).
    """
    declared = any(r is not None for r in (contract_assets, tests, implementations))
    contract_modules: list[types.ModuleType]
    if declared:
        assets = set(contract_assets or ())
        test_roots = set(tests or ())
        impl_roots = set(implementations or ())
        contract_modules = [m for root in sorted(assets) for m in _modules_under(root)]
        test_mods = [m for root in sorted(test_roots) for m in _modules_under(root)]
    else:
        test_mods = list(test_modules)
        assets, test_roots, impl_roots = _derive(test_mods)
        contract_modules = []
        for name in sorted(assets):
            if _ports_root(name):
                contract_modules += list(_modules_under(name))
            else:
                contract_modules.append(sys.modules[name])

    ports_modules = [m for m in contract_modules if _ports_root(m.__name__)]
    contract_only = [m for m in contract_modules if not _ports_root(m.__name__)]
    ports_names = {m.__name__ for m in ports_modules}
    # The package that holds ``ports`` is not itself a contract module, even though
    # ``ports`` lies below it.
    contract_names = {
        m.__name__
        for m in contract_only
        if not any(name.startswith(m.__name__ + ".") for name in ports_names)
    }

    findings: list[Diagnostic] = []
    for module in contract_modules:
        findings += _check_references(module, assets, test_roots, impl_roots)
        findings += _check_structure(module)
    for module in ports_modules:
        findings += _check_ports(module, contract_names)
        findings += _check_ports_parents(module, contract_names)
    for ports_root in sorted({_ports_root(name) or name for name in ports_names}):
        findings += _check_ports_placement(ports_root, test_roots, impl_roots)
        findings += _check_ports_structure(ports_root)
    findings += _check_shapes(contract_only)
    if declared:
        for module in contract_only:
            for root in sorted(_ports_referenced_by([module])):
                if _longest(assets, root) < 0:
                    findings.append(
                        Diagnostic(
                            "ports-undeclared",
                            f"{module.__name__} refers to the boundary types {root}, which is not in the declared range of contract assets",
                            module.__name__,
                        )
                    )
    findings += _check_dependency_cycles(contract_modules)
    findings += _check_tests(test_mods)
    return list(dict.fromkeys(findings))
