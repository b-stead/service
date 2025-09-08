-- name: CreateUser :one
INSERT INTO "user" (
    "sub",
    "email",
    "first_name",
    "last_name",
    "birthdate"
)
VALUES (
    $1,
    $2,
    $3,
    $4,
    $5
) RETURNING *;

-- name: ValidUser :one
SELECT
  "sub"
FROM
  "user"
WHERE
  "sub" = $1
  AND is_deleted = FALSE;

-- name: ListUsers :many
SELECT * FROM "user";

-- name: GetUserBySub :one
SELECT * FROM "user" WHERE "sub" = $1;

-- name: DeleteUserBySub :one
UPDATE "user" SET "is_deleted" = TRUE, "updated_at" = now() , "deleted_at" = now() WHERE "sub" = $1 RETURNING *;

-- name: CreateCustomer :one
INSERT INTO "customers" (
    "user_id",
    "name",
    "company_name",
    "organisation",
    "contact_person",
    "email",
    "phone",
    "address_line1",
    "address_line2",
    "city",
    "state",
    "postal_code",
    "country"
) VALUES (
    (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE),
    $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
) RETURNING *;

-- name: GetCustomerById :one
SELECT * FROM "customers" 
WHERE "user_id" = (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE)
AND "customer_id" = $2 AND "is_deleted" = FALSE;

-- name: ListCustomersBySub :many
SELECT * FROM "customers" 
WHERE "user_id" = (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE)
AND "is_deleted" = FALSE;

-- name: UpdateCustomer :one
UPDATE "customers" 
SET
    "name" = COALESCE($3, "name"),
    "company_name" = COALESCE($4, "company_name"),
    "organisation" = COALESCE($5, "organisation"),
    "contact_person" = COALESCE($6, "contact_person"),
    "email" = COALESCE($7, "email"),
    "phone" = COALESCE($8, "phone"),
    "address_line1" = COALESCE($9, "address_line1"),
    "address_line2" = COALESCE($10, "address_line2"),
    "city" = COALESCE($11, "city"),
    "state" = COALESCE($12, "state"),
    "postal_code" = COALESCE($13, "postal_code"),
    "country" = COALESCE($14, "country"),
    "updated_at" = now()
WHERE 
    "user_id" = (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE)
    AND "customer_id" = $2 AND "is_deleted" = FALSE
RETURNING *;

-- name: DeleteCustomer :one
UPDATE "customers"
SET "is_deleted" = TRUE, "updated_at" = now(), "deleted_at" = now()
WHERE 
    "user_id" = (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE)
    AND "customer_id" = $2 AND "is_deleted" = FALSE
RETURNING *;

-- name: CreateJob :one
INSERT INTO "jobs" (
    "user_id",
    "customer_id",
    "job_title",
    "job_description",
    "job_status",
    "start_date",
    "end_date",
    "estimated_hours",
    "actual_hours",
    "daily_rate",
    "hourly_rate",
    "total_amount"
) VALUES (
    (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE),
    $2, $3, $4, COALESCE($5, 'pending'), $6, $7, $8, $9, $10, $11, $12
) RETURNING *;

-- name: GetJobById :one
SELECT * FROM "jobs" 
WHERE "user_id" = (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE)
AND "job_id" = $2 AND "is_deleted" = FALSE;

-- name: ListJobsBySub :many
SELECT * FROM "jobs" 
WHERE "user_id" = (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE)
AND "is_deleted" = FALSE;

-- name: UpdateJob :one
UPDATE "jobs"
SET
    "customer_id" = COALESCE($3, "customer_id"),
    "job_title" = COALESCE($4, "job_title"),
    "job_description" = COALESCE($5, "job_description"),
    "job_status" = COALESCE($6, "job_status"),
    "start_date" = COALESCE($7, "start_date"),
    "end_date" = COALESCE($8, "end_date"),
    "estimated_hours" = COALESCE($9, "estimated_hours"),
    "actual_hours" = COALESCE($10, "actual_hours"),
    "daily_rate" = COALESCE($11, "daily_rate"),
    "hourly_rate" = COALESCE($12, "hourly_rate"),
    "total_amount" = COALESCE($13, "total_amount"),
    "updated_at" = now()
WHERE 
    "user_id" = (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE)
    AND "job_id" = $2 AND "is_deleted" = FALSE
RETURNING *;

-- name: DeleteJob :one
UPDATE "jobs"
SET "is_deleted" = TRUE, "updated_at" = now(), "deleted_at" = now()
WHERE 
    "user_id" = (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE)
    AND "job_id" = $2 AND "is_deleted" = FALSE
RETURNING *;

-- name: GetJobsByCustomerId :many
SELECT * FROM "jobs" 
WHERE "user_id" = (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE)
AND "customer_id" = $2 AND "is_deleted" = FALSE;

-- name: GetJobsByStatus :many
SELECT * FROM "jobs" 
WHERE "user_id" = (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE)
AND "job_status" = $2 AND "is_deleted" = FALSE;

-- name: GetJobsByDateRange :many
SELECT * FROM "jobs" 
WHERE "user_id" = (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE)
AND "start_date" >= $2 AND "end_date" <= $3 AND "is_deleted" = FALSE;