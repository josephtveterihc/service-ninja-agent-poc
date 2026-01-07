import type { McpToolSchema } from '../types'

export const environmentToolSchemas: McpToolSchema[] = [
  {
    name: 'create_environment',
    description: 'Create a new environment within a project',
    functionName: 'createServiceNinjaEnvironmentTool',
    inputSchema: {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          description: 'Name of the environment to create',
          minLength: 1,
          maxLength: 255,
        },
        description: {
          type: 'string',
          description: 'Description of the environment',
          maxLength: 1000,
        },
        projectId: {
          type: 'number',
          description: 'ID of the project this environment belongs to',
          minimum: 1,
        },
      },
      required: ['name', 'projectId'],
    },
  },
  {
    name: 'list_environments',
    description: 'List all environments, optionally filtered by project',
    functionName: 'getEnvironmentToolListTool',
    inputSchema: {
      type: 'object',
      properties: {
        projectId: {
          type: 'number',
          description: 'Optional project ID to filter environments',
          minimum: 1,
        },
      },
      required: [],
    },
  },
  {
    name: 'get_environment_by_id',
    description: 'Get an environment by its ID',
    functionName: 'readServiceNinjaEnvironmentTool',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the environment to retrieve',
          minimum: 1,
        },
        projectId: {
          type: 'number',
          description: 'Optional project ID to filter by',
          minimum: 1,
        },
      },
      required: ['id'],
    },
  },
  {
    name: 'get_environment_by_name',
    description: 'Get an environment by its name',
    functionName: 'readServiceNinjaEnvironmentTool',
    inputSchema: {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          description: 'Name of the environment to retrieve',
          minLength: 1,
          maxLength: 255,
        },
        projectId: {
          type: 'number',
          description: 'Optional project ID to filter by',
          minimum: 1,
        },
      },
      required: ['name'],
    },
  },
  {
    name: 'update_environment',
    description: 'Update an existing environment',
    functionName: 'updateServiceNinjaEnvironmentTool',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the environment to update',
          minimum: 1,
        },
        name: {
          type: 'string',
          description: 'New name for the environment',
          minLength: 1,
          maxLength: 255,
        },
        description: {
          type: 'string',
          description: 'New description for the environment',
          maxLength: 1000,
        },
        projectId: {
          type: 'number',
          description: 'New project ID (to move environment to different project)',
          minimum: 1,
        },
      },
      required: ['id'],
    },
  },
  {
    name: 'delete_environment',
    description: 'Delete an existing environment',
    functionName: 'deleteServiceNinjaEnvironmentTool',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the environment to delete',
          minimum: 1,
        },
      },
      required: ['id'],
    },
  },
]
