import {
  createServiceNinjaContact,
  deleteServiceNinjaContact,
  getServiceNinjaContact,
  getServiceNinjaContacts,
  searchServiceNinjaContacts,
  updateServiceNinjaContact,
} from '../../repo/service-ninja-repo'
import type { ServiceNinjaContact, CreateServiceNinjaContact } from '../../sql-lite/sql-lite-table.types'
import type { McpToolCallResponse } from '../../types'

export async function createServiceNinjaContactTool(args: CreateServiceNinjaContact): Promise<McpToolCallResponse> {
  console.log('--- createServiceNinjaContactTool --- args:', args)
  const { firstName, lastName, email } = args

  if (!firstName || !lastName || !email) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: 'First name, last name, and email are required.',
        },
      ],
    }
  }

  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email)) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: 'Invalid email format.',
        },
      ],
    }
  }

  // Check if contact with same email already exists
  const existingContact = await getServiceNinjaContact({ email })
  if (existingContact) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Contact with email "${email}" already exists.`,
        },
      ],
    }
  }

  try {
    await createServiceNinjaContact(args)
    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: `Contact "${firstName} ${lastName}" created successfully.`,
        },
      ],
    }
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to create contact: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}

/**
 * Method: readServiceNinjaContactTool
 * Description: Retrieves a specific Service Ninja contact by email or ID.
 * Arguments: An object containing either the contact email or ID.
 * Returns: A promise that resolves to an McpToolCallResponse containing the contact details.
 */
export async function readServiceNinjaContactTool({ email, id }: { email?: string; id?: number }): Promise<McpToolCallResponse> {
  console.log('--- readServiceNinjaContactTool --- args:', { email, id })

  if (!email && !id) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: 'Either email or ID is required.',
        },
      ],
    }
  }

  try {
    const contact = await getServiceNinjaContact({ email, id })

    if (!contact) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `No contact found with ${email ? `email "${email}"` : `ID ${id}`}.`,
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
              id: contact.id,
              firstName: contact.firstName,
              lastName: contact.lastName,
              email: contact.email,
              phone: contact.phone,
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
          text: `Failed to retrieve contact: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}

/**
 * Method: getContactToolListTool
 * Description: Retrieves all Service Ninja contacts from the database.
 * Returns: A promise that resolves to an McpToolCallResponse containing the list of contacts.
 */
export async function getContactToolListTool(): Promise<McpToolCallResponse> {
  console.log('--- getContactToolListTool ---')

  try {
    const contacts = await getServiceNinjaContacts()

    if (!contacts || contacts.length === 0) {
      return {
        isError: false,
        content: [
          {
            type: 'text',
            text: 'No contacts found.',
          },
        ],
      }
    }

    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: JSON.stringify(contacts, null, 2),
        },
      ],
    }
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to retrieve contacts: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}

/**
 * Method: updateServiceNinjaContactTool
 * Description: Updates an existing Service Ninja contact.
 * Arguments: An object containing the contact ID and fields to update.
 * Returns: A promise that resolves to an McpToolCallResponse indicating success.
 */
export async function updateServiceNinjaContactTool(args: Partial<ServiceNinjaContact> & { id: number }): Promise<McpToolCallResponse> {
  console.log('--- updateServiceNinjaContactTool --- args:', args)
  const { id, firstName, lastName, email, phone } = args

  if (!id) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: 'Contact ID is required.',
        },
      ],
    }
  }

  // Check if contact exists
  const existingContact = await getServiceNinjaContact({ id })
  if (!existingContact) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `No contact found with ID ${id}.`,
        },
      ],
    }
  }

  // Validate email format if provided
  if (email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: 'Invalid email format.',
          },
        ],
      }
    }

    // Check if email is already used by another contact
    const contactWithEmail = await getServiceNinjaContact({ email })
    if (contactWithEmail && contactWithEmail.id !== id) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `Email "${email}" is already used by another contact.`,
          },
        ],
      }
    }
  }

  try {
    const res = await updateServiceNinjaContact({ id, firstName, lastName, email, phone } as Partial<ServiceNinjaContact> & { id: number })

    if (!res.success) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: 'Failed to update contact.',
          },
        ],
      }
    }

    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: `Contact updated successfully.`,
        },
      ],
    }
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to update contact: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}

/**
 * Method: deleteServiceNinjaContactTool
 * Description: Deletes a Service Ninja contact.
 * Arguments: An object containing the contact ID.
 * Returns: A promise that resolves to an McpToolCallResponse indicating success.
 */
export async function deleteServiceNinjaContactTool({ id }: { id: number }): Promise<McpToolCallResponse> {
  console.log('--- deleteServiceNinjaContactTool --- args:', { id })

  if (!id) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: 'Contact ID is required.',
        },
      ],
    }
  }

  // Check if contact exists
  const existingContact = await getServiceNinjaContact({ id })
  if (!existingContact) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `No contact found with ID ${id}.`,
        },
      ],
    }
  }

  try {
    const res = await deleteServiceNinjaContact(id)

    if (!res.success) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: 'Failed to delete contact.',
          },
        ],
      }
    }

    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: `Contact "${existingContact.firstName} ${existingContact.lastName}" deleted successfully.`,
        },
      ],
    }
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to delete contact: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}

/**
 * Method: searchServiceNinjaContactsTool
 * Description: Searches Service Ninja contacts by name or email.
 * Arguments: An object containing the search term.
 * Returns: A promise that resolves to an McpToolCallResponse containing matching contacts.
 */
export async function searchServiceNinjaContactsTool({ searchTerm }: { searchTerm: string }): Promise<McpToolCallResponse> {
  console.log('--- searchServiceNinjaContactsTool --- args:', { searchTerm })

  if (!searchTerm || searchTerm.trim().length === 0) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: 'Search term is required.',
        },
      ],
    }
  }

  try {
    const contacts = await searchServiceNinjaContacts(searchTerm)

    if (!contacts || contacts.length === 0) {
      return {
        isError: false,
        content: [
          {
            type: 'text',
            text: `No contacts found matching "${searchTerm}".`,
          },
        ],
      }
    }

    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: JSON.stringify(contacts, null, 2),
        },
      ],
    }
  } catch (error) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to search contacts: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}
