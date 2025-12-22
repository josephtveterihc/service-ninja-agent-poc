import type { McpToolSchema } from '../types'

export const resourceToolSchemas: McpToolSchema[] = [
  {
    name: 'create_resource',
    description: 'Create a new resource within a project environment',
    inputSchema: {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          description: 'Name of the resource to create',
          minLength: 1,
          maxLength: 255,
        },
        description: {
          type: 'string',
          description: 'Description of the resource',
          minLength: 1,
          maxLength: 1000,
        },
        type: {
          type: 'string',
          description: 'Type of the resource (e.g., API, Database, Service)',
          minLength: 1,
          maxLength: 100,
        },
        projectId: {
          type: 'number',
          description: 'ID of the project this resource belongs to',
          minimum: 1,
        },
        envId: {
          type: 'number',
          description: 'ID of the environment this resource belongs to',
          minimum: 1,
        },
        healthCheckUrl: {
          type: 'string',
          description: 'Optional health check URL for the resource',
          format: 'uri',
          maxLength: 2048,
        },
        aliveCheckUrl: {
          type: 'string',
          description: 'Optional alive check URL for the resource',
          format: 'uri',
          maxLength: 2048,
        },
        headers: {
          type: 'string',
          description: 'Optional headers as JSON string for requests',
          maxLength: 4096,
        },
        isIhService: {
          type: 'boolean',
          description: 'Whether this is an IH service',
        },
      },
      required: ['name', 'description', 'type', 'projectId', 'envId'],
    },
  },
  {
    name: 'list_resources',
    description: 'List all resources, optionally filtered by project and/or environment',
    inputSchema: {
      type: 'object',
      properties: {
        projectId: {
          type: 'number',
          description: 'Optional project ID to filter resources',
          minimum: 1,
        },
        envId: {
          type: 'number',
          description: 'Optional environment ID to filter resources',
          minimum: 1,
        },
      },
      required: [],
    },
  },
  {
    name: 'get_resource_by_id',
    description: 'Get a resource by its ID',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the resource to retrieve',
          minimum: 1,
        },
        projectId: {
          type: 'number',
          description: 'Optional project ID to filter by',
          minimum: 1,
        },
        envId: {
          type: 'number',
          description: 'Optional environment ID to filter by',
          minimum: 1,
        },
      },
      required: ['id'],
    },
  },
  {
    name: 'get_resource_by_name',
    description: 'Get a resource by its name',
    inputSchema: {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          description: 'Name of the resource to retrieve',
          minLength: 1,
          maxLength: 255,
        },
        projectId: {
          type: 'number',
          description: 'Optional project ID to filter by',
          minimum: 1,
        },
        envId: {
          type: 'number',
          description: 'Optional environment ID to filter by',
          minimum: 1,
        },
      },
      required: ['name'],
    },
  },
  {
    name: 'update_resource',
    description: 'Update an existing resource',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the resource to update',
          minimum: 1,
        },
        name: {
          type: 'string',
          description: 'New name for the resource',
          minLength: 1,
          maxLength: 255,
        },
        description: {
          type: 'string',
          description: 'New description for the resource',
          minLength: 1,
          maxLength: 1000,
        },
        type: {
          type: 'string',
          description: 'New type for the resource',
          minLength: 1,
          maxLength: 100,
        },
        projectId: {
          type: 'number',
          description: 'New project ID (to move resource to different project)',
          minimum: 1,
        },
        envId: {
          type: 'number',
          description: 'New environment ID (to move resource to different environment)',
          minimum: 1,
        },
        healthCheckUrl: {
          type: 'string',
          description: 'New health check URL for the resource',
          format: 'uri',
          maxLength: 2048,
        },
        aliveCheckUrl: {
          type: 'string',
          description: 'New alive check URL for the resource',
          format: 'uri',
          maxLength: 2048,
        },
        headers: {
          type: 'string',
          description: 'New headers as JSON string for requests',
          maxLength: 4096,
        },
        isIhService: {
          type: 'boolean',
          description: 'Whether this is an IH service',
        },
      },
      required: ['id'],
    },
  },
  {
    name: 'delete_resource',
    description: 'Delete an existing resource',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the resource to delete',
          minimum: 1,
        },
      },
      required: ['id'],
    },
  },
]
