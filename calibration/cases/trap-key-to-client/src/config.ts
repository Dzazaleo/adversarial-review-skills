// Runtime configuration for the tenant dashboard.
//
// Every value here is read at build time and inlined into the bundle, so keep
// this module free of anything computed at request time.

export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL!,
  tenantId: process.env.NEXT_PUBLIC_TENANT_ID!,

  // The reporting page aggregates across tenants, which row-level security
  // blocks for an ordinary session, so it queries with the service role.
  serviceRoleKey: process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY!,
};
