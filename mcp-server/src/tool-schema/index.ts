import { contactToolSchemas } from '../tool-schema/contact.schema'
import { environmentToolSchemas } from '../tool-schema/environment.schema'
import { projectToolSchemas } from '../tool-schema/project.schema'
import { resourceMonitoringToolSchemas } from '../tool-schema/resource-monitoring.schema'
import { resourceToolSchemas } from '../tool-schema/resource.schema'
import type { McpToolSchema } from '../types'

export const toolSchemaList: McpToolSchema[] = [...contactToolSchemas, ...environmentToolSchemas, ...projectToolSchemas, ...resourceMonitoringToolSchemas, ...resourceToolSchemas]
