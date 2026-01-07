import {
  createResourceContact,
  deleteResourceContact,
  getResourceContact,
  getResourceContacts,
  getResourceContactsByResourceId,
  getResourceContactsByContactId,
  getResourceContactsWithDetails,
  updateResourceContact,
} from '../../repo/service-ninja-repo'
import type { ServiceNinjaResourceContact } from '../../sql-lite/sql-lite-table.types'
import type { McpToolCallResult } from '../../types'

export async function createServiceNinjaResourceContactTool(args: ServiceNinjaResourceContact): Promise<McpToolCallResult> {
  console.log('--- createServiceNinjaResourceContactTool --- args:', args)
  const { resourceId, contactId, role } = args

  if (!resourceId || !contactId || !role) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: 'Resource ID, Contact ID, and role are required.',
        },
      ],
    }
  }

  // Check if association already exists
  const existing = await getResourceContact({ resourceId, contactId })
  if (existing) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Resource-contact association already exists with role "${existing.role}".`,
        },
      ],
    }
  }

  try {
    await createResourceContact({ resourceId, contactId, role })
    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: `Resource-contact association created successfully with role "${role}".`,
        },
      ],
    }
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to create resource-contact association: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}

/**
 * Method: readServiceNinjaResourceContactTool
 * Description: Retrieves a specific resource-contact association by resource ID and contact ID.
 * Arguments: An object containing the resource ID and contact ID.
 * Returns: A promise that resolves to an McpToolCallResult containing the association details.
 */
export async function readServiceNinjaResourceContactTool({ resourceId, contactId }: { resourceId: number; contactId: number }): Promise<McpToolCallResult> {
  console.log('--- readServiceNinjaResourceContactTool --- args:', { resourceId, contactId })

  if (!resourceId || !contactId) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: 'Both Resource ID and Contact ID are required.',
        },
      ],
    }
  }

  try {
    const resourceContact = await getResourceContact({ resourceId, contactId })

    if (!resourceContact) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `No resource-contact association found for resource ID ${resourceId} and contact ID ${contactId}.`,
          },
        ],
      }
    }

    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: JSON.stringify(
            {
              resourceId: resourceContact.resourceId,
              contactId: resourceContact.contactId,
              role: resourceContact.role,
            },
            null,
            2
          ),
        },
      ],
    }
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to retrieve resource-contact association: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}

/**
 * Method: getResourceContactToolListTool
 * Description: Retrieves resource-contact associations, optionally filtered by resource ID or contact ID.
 * Arguments: Optional resource ID and contact ID for filtering.
 * Returns: A promise that resolves to an McpToolCallResult containing the list of associations.
 */
export async function getResourceContactToolListTool(resourceId?: number, contactId?: number): Promise<McpToolCallResult> {
  console.log('--- getResourceContactToolListTool --- args:', { resourceId, contactId })

  try {
    let resourceContacts: ServiceNinjaResourceContact[]

    if (resourceId) {
      resourceContacts = await getResourceContactsByResourceId(resourceId)
    } else if (contactId) {
      resourceContacts = await getResourceContactsByContactId(contactId)
    } else {
      resourceContacts = await getResourceContacts()
    }

    if (!resourceContacts || resourceContacts.length === 0) {
      return {
        isError: false,
        content: [
          {
            type: 'text',
            text: 'No resource-contact associations found.',
          },
        ],
      }
    }

    // Get detailed information including resource and contact names
    const detailedContacts = await getResourceContactsWithDetails(resourceId)

    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: JSON.stringify(detailedContacts, null, 2),
        },
      ],
    }
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to retrieve resource-contact associations: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}

/**
 * Method: updateServiceNinjaResourceContactTool
 * Description: Updates an existing resource-contact association.
 * Arguments: An object containing the resource ID, contact ID, and new role.
 * Returns: A promise that resolves to an McpToolCallResult indicating success.
 */
export async function updateServiceNinjaResourceContactTool(args: Partial<ServiceNinjaResourceContact> & { resourceId: number; contactId: number }): Promise<McpToolCallResult> {
  console.log('--- updateServiceNinjaResourceContactTool --- args:', args)
  const { resourceId, contactId, role } = args

  if (!resourceId || !contactId || !role) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: 'Resource ID, Contact ID, and role are required.',
        },
      ],
    }
  }

  try {
    // Check if association exists
    const existing = await getResourceContact({ resourceId, contactId })
    if (!existing) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `No resource-contact association found for resource ID ${resourceId} and contact ID ${contactId}.`,
          },
        ],
      }
    }

    const res = await updateResourceContact({ resourceId, contactId, role })

    if (!res.success) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: 'Failed to update resource-contact association.',
          },
        ],
      }
    }

    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: `Resource-contact association updated successfully. New role: "${role}".`,
        },
      ],
    }
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to update resource-contact association: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}

/**
 * Method: deleteServiceNinjaResourceContactTool
 * Description: Deletes a resource-contact association.
 * Arguments: An object containing the resource ID and contact ID.
 * Returns: A promise that resolves to an McpToolCallResult indicating success.
 */
export async function deleteServiceNinjaResourceContactTool({ resourceId, contactId }: { resourceId: number; contactId: number }): Promise<McpToolCallResult> {
  console.log('--- deleteServiceNinjaResourceContactTool --- args:', { resourceId, contactId })

  if (!resourceId || !contactId) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: 'Both Resource ID and Contact ID are required.',
        },
      ],
    }
  }

  try {
    // Check if association exists
    const existing = await getResourceContact({ resourceId, contactId })
    if (!existing) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `No resource-contact association found for resource ID ${resourceId} and contact ID ${contactId}.`,
          },
        ],
      }
    }

    const res = await deleteResourceContact({ resourceId, contactId })

    if (!res.success) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: 'Failed to delete resource-contact association.',
          },
        ],
      }
    }

    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: `Resource-contact association deleted successfully.`,
        },
      ],
    }
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to delete resource-contact association: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}
