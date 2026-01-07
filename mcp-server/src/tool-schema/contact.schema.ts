import type { McpToolSchema } from '../types'

export const contactToolSchemas: McpToolSchema[] = [
  {
    name: 'create_contact',
    description: 'Create a new contact',
    functionName: 'createServiceNinjaContactTool',
    inputSchema: {
      type: 'object',
      properties: {
        firstName: {
          type: 'string',
          description: 'First name of the contact',
          minLength: 1,
          maxLength: 100,
        },
        lastName: {
          type: 'string',
          description: 'Last name of the contact',
          minLength: 1,
          maxLength: 100,
        },
        email: {
          type: 'string',
          description: 'Email address of the contact',
          format: 'email',
          minLength: 5,
          maxLength: 255,
        },
        phone: {
          type: 'string',
          description: 'Phone number of the contact (optional)',
          maxLength: 20,
        },
      },
      required: ['firstName', 'lastName', 'email'],
    },
  },
  {
    name: 'list_contacts',
    description: 'List all contacts',
    functionName: 'getContactToolListTool',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'get_contact_by_id',
    description: 'Get a contact by its ID',
    functionName: 'readServiceNinjaContactTool',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the contact to retrieve',
          minimum: 1,
        },
      },
      required: ['id'],
    },
  },
  {
    name: 'get_contact_by_email',
    description: 'Get a contact by its email address',
    functionName: 'readServiceNinjaContactTool',
    inputSchema: {
      type: 'object',
      properties: {
        email: {
          type: 'string',
          description: 'Email address of the contact to retrieve',
          format: 'email',
          minLength: 5,
          maxLength: 255,
        },
      },
      required: ['email'],
    },
  },
  {
    name: 'update_contact',
    description: 'Update an existing contact',
    functionName: 'updateServiceNinjaContactTool',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the contact to update',
          minimum: 1,
        },
        firstName: {
          type: 'string',
          description: 'New first name for the contact',
          minLength: 1,
          maxLength: 100,
        },
        lastName: {
          type: 'string',
          description: 'New last name for the contact',
          minLength: 1,
          maxLength: 100,
        },
        email: {
          type: 'string',
          description: 'New email address for the contact',
          format: 'email',
          minLength: 5,
          maxLength: 255,
        },
        phone: {
          type: 'string',
          description: 'New phone number for the contact',
          maxLength: 20,
        },
      },
      required: ['id'],
    },
  },
  {
    name: 'delete_contact',
    description: 'Delete an existing contact',
    functionName: 'deleteServiceNinjaContactTool',
    inputSchema: {
      type: 'object',
      properties: {
        id: {
          type: 'number',
          description: 'ID of the contact to delete',
          minimum: 1,
        },
      },
      required: ['id'],
    },
  },
  {
    name: 'search_contacts',
    description: 'Search contacts by name or email',
    functionName: 'searchServiceNinjaContactsTool',
    inputSchema: {
      type: 'object',
      properties: {
        searchTerm: {
          type: 'string',
          description: 'Search term to match against firstName, lastName, or email',
          minLength: 1,
          maxLength: 255,
        },
      },
      required: ['searchTerm'],
    },
  },
  {
    name: 'create_resource_contact',
    description: 'Create a new resource-contact association',
    functionName: 'createServiceNinjaResourceContactTool',
    inputSchema: {
      type: 'object',
      properties: {
        resourceId: {
          type: 'number',
          description: 'ID of the resource',
          minimum: 1,
        },
        contactId: {
          type: 'number',
          description: 'ID of the contact',
          minimum: 1,
        },
        role: {
          type: 'string',
          description: 'Role of the contact for this resource (e.g., "owner", "maintainer", "developer", "support")',
          minLength: 1,
          maxLength: 100,
        },
      },
      required: ['resourceId', 'contactId', 'role'],
    },
  },
  {
    name: 'list_resource_contacts',
    description: 'List resource-contact associations, optionally filtered by resource or contact',
    functionName: 'getResourceContactToolListTool',
    inputSchema: {
      type: 'object',
      properties: {
        resourceId: {
          type: 'number',
          description: 'ID of the resource to filter by (optional)',
          minimum: 1,
        },
        contactId: {
          type: 'number',
          description: 'ID of the contact to filter by (optional)',
          minimum: 1,
        },
      },
      required: [],
    },
  },
  {
    name: 'get_resource_contact_by_ids',
    description: 'Get a specific resource-contact association by resource ID and contact ID',
    functionName: 'readServiceNinjaResourceContactTool',
    inputSchema: {
      type: 'object',
      properties: {
        resourceId: {
          type: 'number',
          description: 'ID of the resource',
          minimum: 1,
        },
        contactId: {
          type: 'number',
          description: 'ID of the contact',
          minimum: 1,
        },
      },
      required: ['resourceId', 'contactId'],
    },
  },
  {
    name: 'update_resource_contact',
    description: 'Update the role of an existing resource-contact association',
    functionName: 'updateServiceNinjaResourceContactTool',
    inputSchema: {
      type: 'object',
      properties: {
        resourceId: {
          type: 'number',
          description: 'ID of the resource',
          minimum: 1,
        },
        contactId: {
          type: 'number',
          description: 'ID of the contact',
          minimum: 1,
        },
        role: {
          type: 'string',
          description: 'New role for the contact-resource association',
          minLength: 1,
          maxLength: 100,
        },
      },
      required: ['resourceId', 'contactId', 'role'],
    },
  },
  {
    name: 'delete_resource_contact',
    description: 'Delete a resource-contact association',
    functionName: 'deleteServiceNinjaResourceContactTool',
    inputSchema: {
      type: 'object',
      properties: {
        resourceId: {
          type: 'number',
          description: 'ID of the resource',
          minimum: 1,
        },
        contactId: {
          type: 'number',
          description: 'ID of the contact',
          minimum: 1,
        },
      },
      required: ['resourceId', 'contactId'],
    },
  },
]
