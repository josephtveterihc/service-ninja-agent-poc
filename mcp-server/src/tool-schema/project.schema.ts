import type { McpToolSchema } from '../types'

export const projectToolSchemas: McpToolSchema[] = [
  {
    name: 'create_project',
    description: 'Create a new project',
    functionName: 'createServiceNinjaProjectTool',
    inputSchema: {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          description: 'Name of the project to create',
          minLength: 1,
          maxLength: 255,
        },
        description: {
          type: 'string',
          description: 'Description of the project',
          minLength: 1,
          maxLength: 1000,
        },
      },
      required: ['name', 'description'],
    },
  },
  {
    name: 'list_projects',
    description: 'List all projects',
    functionName: 'getProjectToolListTool',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'update_project',
    description: 'Update an existing project',
    functionName: 'updateServiceNinjaProjectTool',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the project to update',
          minimum: 1,
        },
        name: {
          type: 'string',
          description: 'New name for the project',
          minLength: 1,
          maxLength: 255,
        },
        description: {
          type: 'string',
          description: 'New description for the project',
          minLength: 1,
          maxLength: 1000,
        },
      },
      required: ['id'],
    },
  },
  {
    name: 'delete_project',
    description: 'Delete an existing project',
    functionName: 'deleteServiceNinjaProjectTool',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the project to delete',
          minimum: 1,
        },
      },
      required: ['id'],
    },
  },
  {
    name: 'get_project_by_name',
    description: 'Get a project by its name',
    functionName: 'readServiceNinjaProjectTool',
    inputSchema: {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          description: 'Name of the project to retrieve',
          minLength: 1,
          maxLength: 255,
        },
      },
      required: ['name'],
    },
  },
  {
    name: 'get_project_by_id',
    description: 'Get a project by its ID',
    functionName: 'readServiceNinjaProjectTool',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the project to retrieve',
          minimum: 1,
        },
      },
      required: ['id'],
    },
  },
]
