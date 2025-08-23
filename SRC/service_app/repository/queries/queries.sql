-- name: CreateUser :one
INSERT INTO "user" (
    "sub",
    "email",
    "email_verified",
    "first_name",
    "last_name",
    "birthdate"
)
VALUES (
    $1,
    $2,
    $3,
    $4,
    $5,
    $6
) RETURNING *;