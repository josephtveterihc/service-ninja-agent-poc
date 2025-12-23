import {
  createServiceNinjaResource,
  deleteServiceNinjaResource,
  getServiceNinjaResource,
  getServiceNinjaResources,
  updateServiceNinjaResource,
} from '../../repo/service-ninja-repo'
import type { ServiceNinjaResource } from '../../sql-lite/sql-lite-table.types'
import type { McpToolCallResponse } from '../../types'

export async function createServiceNinjaResourceTool(args: Partial<ServiceNinjaResource>): Promise<McpToolCallResponse> {
  const { name, projectId, envId } = args
  const resources = await getServiceNinjaResources(projectId, envId)
  const existingResource = resources.find((resource: { name: string }) => resource.name.toLowerCase() === name?.toLowerCase())

  if (existingResource) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Resource with name "${name}" already exists in this environment.`,
        },
      ],
    }
  }
  const res = await createServiceNinjaResource(args)

  return {
    isError: false,
    content: [
      {
        type: 'text',
        text: `Resource "${name}" created successfully with ID ${res.success}.`,
      },
    ],
  }
}

/**
 * Method: readServiceNinjaResourceTool
 * Description: Retrieves a specific Service Ninja resource by name or ID.
 * Arguments: An object containing either the resource name or ID, and optionally projectId and envId.
 * Returns: A promise that resolves to an McpToolCallResponse containing the resource details.
 */
export async function readServiceNinjaResourceTool({
  name,
  id,
  projectId,
  envId,
}: {
  name?: string
  id?: number
  projectId?: number
  envId?: number
}): Promise<McpToolCallResponse> {
  console.log('--- readServiceNinjaResourceTool ---', { name, id, projectId, envId })
  const resource = await getServiceNinjaResource({ name, id, projectId, envId })

  if (!resource) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Resource not found.`,
        },
      ],
    }
  }

  return {
    isError: false,
    content: [
      {
        type: 'text',
        data: JSON.stringify({ resource }),
        text: `Resource details retrieved successfully.`,
      },
    ],
  }
}

/**
 * Method: updateServiceNinjaResourceTool
 * Description: Updates an existing Service Ninja resource.
 * Arguments: An object containing the resource ID and fields to update.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function updateServiceNinjaResourceTool(params: Partial<ServiceNinjaResource> & { id: number }): Promise<McpToolCallResponse> {
  console.log('--- updateServiceNinjaResourceTool --- params:', params)
  const res = await updateServiceNinjaResource(params)
  return { isError: false, content: [{ type: 'text', text: res?.success ? `Resource updated successfully.` : `Failed to update resource.` }] }
}

/**
 * Method: deleteServiceNinjaResourceTool
 * Description: Deletes a specific Service Ninja resource by ID.
 * Arguments: An object containing the resource ID.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function deleteServiceNinjaResourceTool(params: { id: number }): Promise<McpToolCallResponse> {
  console.log('--- deleteServiceNinjaResourceTool --- params:', params)
  const res = await deleteServiceNinjaResource(params.id)
  return { isError: false, content: [{ type: 'text', text: `Resource deleted successfully.` }] }
}

/**
 * Method: getResourceToolListTool
 * Description: Retrieves the list of Service Ninja resources from the database, optionally filtered by project and/or environment.
 * Arguments: Optional projectId and envId for filtering.
 * Returns: A promise that resolves to an McpToolCallResponse containing the list of resources.
 */
export async function getResourceToolListTool(projectId?: number, envId?: number): Promise<McpToolCallResponse> {
  console.log('--- getResourceToolListTool --- projectId:', projectId, 'envId:', envId)
  const resources = await getServiceNinjaResources(projectId, envId)
  return {
    isError: false,
    content: [
      {
        type: 'text',
        data: JSON.stringify({ resources }),
        text: `Resource list retrieved successfully.`,
      },
    ],
  }
}
