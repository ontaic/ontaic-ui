"""GraphQL integration for ontaic."""
import json
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class OperationType(str, Enum):
    """GraphQL operation types."""
    QUERY = "query"
    MUTATION = "mutation"
    SUBSCRIPTION = "subscription"


@dataclass
class GraphQLField:
    """GraphQL field definition."""
    name: str
    alias: Optional[str] = None
    arguments: Dict[str, Any] = field(default_factory=dict)
    selections: List["GraphQLField"] = field(default_factory=list)
    
    def to_query(self, indent: int = 0) -> str:
        """Convert to GraphQL query string."""
        prefix = "  " * indent
        alias = f"{self.alias}: " if self.alias else ""
        
        if self.arguments:
            args = ", ".join(f'{k}: {json.dumps(v) if isinstance(v, (str, int, float, bool)) else v}' for k, v in self.arguments.items())
            field_str = f"{prefix}{alias}{self.name}({args})"
        else:
            field_str = f"{prefix}{alias}{self.name}"
        
        if self.selections:
            selections_str = "\n".join(s.to_query(indent + 1) for s in self.selections)
            return f"{field_str} {{\n{selections_str}\n{prefix}}}"
        
        return field_str


@dataclass
class GraphQLOperation:
    """GraphQL operation."""
    name: str
    operation_type: OperationType
    fields: List[GraphQLField]
    variables: Dict[str, str] = field(default_factory=dict)
    
    def to_query(self) -> str:
        """Convert to GraphQL query string."""
        var_defs = ""
        if self.variables:
            vars = ", ".join(f"${k}: {v}" for k, v in self.variables.items())
            var_defs = f"({vars})"
        
        fields_str = "\n    ".join(f.to_query(1) for f in self.fields)
        
        return f"""{self.operation_type.value} {self.name}{var_defs} {{
    {fields_str}
}}"""


@dataclass
class GraphQLResponse:
    """GraphQL response."""
    data: Optional[Dict[str, Any]] = None
    errors: List[Dict[str, Any]] = field(default_factory=list)
    
    @property
    def success(self) -> bool:
        return len(self.errors) == 0
    
    @property
    def error_message(self) -> str:
        if not self.errors:
            return ""
        return "\n".join(e.get("message", "Unknown error") for e in self.errors)


class GraphQLClient:
    """GraphQL client for making requests."""
    
    def __init__(self, endpoint: str, headers: Dict[str, str] = None):
        self.endpoint = endpoint
        self.headers = headers or {}
        self._interceptors: List[Callable] = []
    
    def add_interceptor(self, interceptor: Callable):
        """Add request interceptor."""
        self._interceptors.append(interceptor)
    
    async def execute(self, query: str, variables: Dict[str, Any] = None, operation_name: str = None) -> GraphQLResponse:
        """Execute a GraphQL operation."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        if operation_name:
            payload["operationName"] = operation_name
        
        # Run interceptors
        for interceptor in self._interceptors:
            result = interceptor(payload)
            if result is False:
                return GraphQLResponse(errors=[{"message": "Request blocked by interceptor"}])
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.endpoint,
                    json=payload,
                    headers={**self.headers, "Content-Type": "application/json"}
                ) as resp:
                    data = await resp.json()
                    return GraphQLResponse(
                        data=data.get("data"),
                        errors=data.get("errors", [])
                    )
        except ImportError:
            return GraphQLResponse(errors=[{"message": "aiohttp not installed. Run: pip install aiohttp"}])
        except Exception as e:
            return GraphQLResponse(errors=[{"message": str(e)}])
    
    def execute_sync(self, query: str, variables: Dict[str, Any] = None, operation_name: str = None) -> GraphQLResponse:
        """Execute a GraphQL operation synchronously."""
        import requests
        
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        if operation_name:
            payload["operationName"] = operation_name
        
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers={**self.headers, "Content-Type": "application/json"}
            )
            data = response.json()
            return GraphQLResponse(
                data=data.get("data"),
                errors=data.get("errors", [])
            )
        except Exception as e:
            return GraphQLResponse(errors=[{"message": str(e)}])
    
    def query(self, name: str, fields: List[GraphQLField], variables: Dict[str, str] = None) -> GraphQLOperation:
        """Create a query operation."""
        return GraphQLOperation(
            name=name,
            operation_type=OperationType.QUERY,
            fields=fields,
            variables=variables or {},
        )
    
    def mutation(self, name: str, fields: List[GraphQLField], variables: Dict[str, str] = None) -> GraphQLOperation:
        """Create a mutation operation."""
        return GraphQLOperation(
            name=name,
            operation_type=OperationType.MUTATION,
            fields=fields,
            variables=variables or {},
        )
    
    def subscription(self, name: str, fields: List[GraphQLField], variables: Dict[str, str] = None) -> GraphQLOperation:
        """Create a subscription operation."""
        return GraphQLOperation(
            name=name,
            operation_type=OperationType.SUBSCRIPTION,
            fields=fields,
            variables=variables or {},
        )


class GraphQLQueryBuilder:
    """Builder for constructing GraphQL queries."""
    
    def __init__(self, operation_type: OperationType = OperationType.QUERY, name: str = ""):
        self.operation_type = operation_type
        self.name = name
        self._fields: List[GraphQLField] = []
        self._variables: Dict[str, str] = {}
        self._fragments: Dict[str, List[GraphQLField]] = {}
    
    def field(self, name: str, alias: str = None, arguments: Dict[str, Any] = None, selections: List[GraphQLField] = None) -> "GraphQLQueryBuilder":
        """Add a field."""
        self._fields.append(GraphQLField(
            name=name,
            alias=alias,
            arguments=arguments or {},
            selections=selections or [],
        ))
        return self
    
    def variable(self, name: str, type_name: str) -> "GraphQLQueryBuilder":
        """Add a variable."""
        self._variables[name] = type_name
        return self
    
    def fragment(self, name: str, fields: List[GraphQLField]) -> "GraphQLQueryBuilder":
        """Define a fragment."""
        self._fragments[name] = fields
        return self
    
    def build(self) -> GraphQLOperation:
        """Build the operation."""
        return GraphQLOperation(
            name=self.name,
            operation_type=self.operation_type,
            fields=self._fields,
            variables=self._variables,
        )
    
    def build_query(self) -> str:
        """Build query string."""
        return self.build().to_query()


class GraphQLSchemaBuilder:
    """Builder for GraphQL schemas."""
    
    def __init__(self):
        self._types: Dict[str, Dict[str, Any]] = {}
        self._queries: Dict[str, Dict[str, Any]] = {}
        self._mutations: Dict[str, Dict[str, Any]] = {}
        self._subscriptions: Dict[str, Dict[str, Any]] = {}
    
    def type(self, name: str, fields: Dict[str, str], interfaces: List[str] = None) -> "GraphQLSchemaBuilder":
        """Define a GraphQL type."""
        self._types[name] = {"fields": fields, "interfaces": interfaces or []}
        return self
    
    def input(self, name: str, fields: Dict[str, str]) -> "GraphQLSchemaBuilder":
        """Define a GraphQL input type."""
        self._types[name] = {"fields": fields, "is_input": True}
        return self
    
    def enum(self, name: str, values: List[str]) -> "GraphQLSchemaBuilder":
        """Define a GraphQL enum."""
        self._types[name] = {"values": values, "is_enum": True}
        return self
    
    def query(self, name: str, return_type: str, arguments: Dict[str, str] = None) -> "GraphQLSchemaBuilder":
        """Define a query field."""
        self._queries[name] = {"return_type": return_type, "arguments": arguments or {}}
        return self
    
    def mutation(self, name: str, return_type: str, arguments: Dict[str, str] = None) -> "GraphQLSchemaBuilder":
        """Define a mutation field."""
        self._mutations[name] = {"return_type": return_type, "arguments": arguments or {}}
        return self
    
    def subscription(self, name: str, return_type: str, arguments: Dict[str, str] = None) -> "GraphQLSchemaBuilder":
        """Define a subscription field."""
        self._subscriptions[name] = {"return_type": return_type, "arguments": arguments or {}}
        return self
    
    def build(self) -> str:
        """Build the GraphQL schema string."""
        lines = []
        
        # Types
        for name, type_def in self._types.items():
            if type_def.get("is_enum"):
                lines.append(f"enum {name} {{")
                for value in type_def["values"]:
                    lines.append(f"  {value}")
                lines.append("}\n")
            elif type_def.get("is_input"):
                lines.append(f"input {name} {{")
                for field_name, field_type in type_def["fields"].items():
                    lines.append(f"  {field_name}: {field_type}")
                lines.append("}\n")
            else:
                if type_def["interfaces"]:
                    interfaces = ", ".join(type_def["interfaces"])
                    lines.append(f"type {name} implements {interfaces} {{")
                else:
                    lines.append(f"type {name} {{")
                for field_name, field_type in type_def["fields"].items():
                    lines.append(f"  {field_name}: {field_type}")
                lines.append("}\n")
        
        # Query
        if self._queries:
            lines.append("type Query {")
            for name, query_def in self._queries.items():
                args = ""
                if query_def["arguments"]:
                    args = "(" + ", ".join(f"{k}: {v}" for k, v in query_def["arguments"].items()) + ")"
                lines.append(f"  {name}{args}: {query_def['return_type']}")
            lines.append("}\n")
        
        # Mutation
        if self._mutations:
            lines.append("type Mutation {")
            for name, mutation_def in self._mutations.items():
                args = ""
                if mutation_def["arguments"]:
                    args = "(" + ", ".join(f"{k}: {v}" for k, v in mutation_def["arguments"].items()) + ")"
                lines.append(f"  {name}{args}: {mutation_def['return_type']}")
            lines.append("}\n")
        
        # Subscription
        if self._subscriptions:
            lines.append("type Subscription {")
            for name, sub_def in self._subscriptions.items():
                args = ""
                if sub_def["arguments"]:
                    args = "(" + ", ".join(f"{k}: {v}" for k, v in sub_def["arguments"].items()) + ")"
                lines.append(f"  {name}{args}: {sub_def['return_type']}")
            lines.append("}\n")
        
        return "\n".join(lines)


def gql_query(name: str) -> Callable:
    """Decorator to define a GraphQL query."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper._gql_operation_type = OperationType.QUERY
        wrapper._gql_name = name
        return wrapper
    return decorator


def gql_mutation(name: str) -> Callable:
    """Decorator to define a GraphQL mutation."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper._gql_operation_type = OperationType.MUTATION
        wrapper._gql_name = name
        return wrapper
    return decorator


def gql_subscription(name: str) -> Callable:
    """Decorator to define a GraphQL subscription."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper._gql_operation_type = OperationType.SUBSCRIPTION
        wrapper._gql_name = name
        return wrapper
    return decorator


def create_gql_client(endpoint: str, headers: Dict[str, str] = None) -> GraphQLClient:
    """Create a GraphQL client."""
    return GraphQLClient(endpoint, headers)


def build_schema() -> GraphQLSchemaBuilder:
    """Create a schema builder."""
    return GraphQLSchemaBuilder()


def build_query(name: str) -> GraphQLQueryBuilder:
    """Create a query builder."""
    return GraphQLQueryBuilder(OperationType.QUERY, name)


def build_mutation(name: str) -> GraphQLQueryBuilder:
    """Create a mutation builder."""
    return GraphQLQueryBuilder(OperationType.MUTATION, name)
