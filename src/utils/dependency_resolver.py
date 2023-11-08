
def resolve_dependencies(agent_params, variable_store):
    """Resolves the dependencies of an agent."""
    dependencies = {}
    if agent_params.dependencies:
        for dependency in agent_params.dependencies:
            dependencies[dependency] = variable_store.get_variable(dependency)
    return dependencies

