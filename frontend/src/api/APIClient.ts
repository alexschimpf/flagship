/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BaseHttpRequest } from './core/BaseHttpRequest';
import type { OpenAPIConfig } from './core/OpenAPI';
import { AxiosHttpRequest } from './core/AxiosHttpRequest';
import { AdminService } from './services/AdminService';
import { AuthService } from './services/AuthService';
import { ContextFieldsService } from './services/ContextFieldsService';
import { FeatureFlagsService } from './services/FeatureFlagsService';
import { ProjectsService } from './services/ProjectsService';
import { UsersService } from './services/UsersService';
type HttpRequestConstructor = new (config: OpenAPIConfig) => BaseHttpRequest;
export class APIClient {
    public readonly admin: AdminService;
    public readonly auth: AuthService;
    public readonly contextFields: ContextFieldsService;
    public readonly featureFlags: FeatureFlagsService;
    public readonly projects: ProjectsService;
    public readonly users: UsersService;
    public readonly request: BaseHttpRequest;
    constructor(config?: Partial<OpenAPIConfig>, HttpRequest: HttpRequestConstructor = AxiosHttpRequest) {
        this.request = new HttpRequest({
            BASE: config?.BASE ?? '',
            VERSION: config?.VERSION ?? '1.0',
            WITH_CREDENTIALS: config?.WITH_CREDENTIALS ?? false,
            CREDENTIALS: config?.CREDENTIALS ?? 'include',
            TOKEN: config?.TOKEN,
            USERNAME: config?.USERNAME,
            PASSWORD: config?.PASSWORD,
            HEADERS: config?.HEADERS,
            ENCODE_PATH: config?.ENCODE_PATH,
        });
        this.admin = new AdminService(this.request);
        this.auth = new AuthService(this.request);
        this.contextFields = new ContextFieldsService(this.request);
        this.featureFlags = new FeatureFlagsService(this.request);
        this.projects = new ProjectsService(this.request);
        this.users = new UsersService(this.request);
    }
}

