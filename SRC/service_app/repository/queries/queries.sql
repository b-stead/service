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

-- name: GetCustomersByUserSub :many
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