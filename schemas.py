from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Str(required=True)
    account_created_date = fields.Str(required=True)
    is_staff = fields.Str(required=True)

class UserLogInOutSchma(Schema):
    username = fields.Str()
    password = fields.Str()

class PlainUserTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    task_id = fields.Int()
    occurrence_type = fields.Str(required=True)
    scoring = fields.Str(required=True)
    status = fields.Str(required=True)
    start_datetime = fields.Str(required=True)
    due_datetime = fields.Str(required=True)

class UserSchema(PlainUserSchema):
    usertask = fields.List(fields.Nested(PlainUserTaskSchema()), dump_only=True)

class UserUpdateSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    email = fields.Str()
    is_staff = fields.Str()

class PlainProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    project_name = fields.Str(required=True)
    description = fields.Str(required=True)

class PlainTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    task_name = fields.Str(required=True)
    description = fields.Str(required=True)

class TaskSchema(PlainTaskSchema):
    usertask_id = fields.Int(required=False, load_only=True)
    usertask = fields.Nested(PlainTaskSchema(), dump_only=True)

class UserTaskSchema(PlainUserTaskSchema):
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)

    # task = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)
    task = fields.Nested(PlainTaskSchema(), dump_only=True)
    projects = fields.List(fields.Nested(PlainProjectSchema()), dump_only=True)

class ProjectSchema(PlainProjectSchema):
    usertasks = fields.List(fields.Nested(PlainUserTaskSchema()), dump_only=True)

class ProjectUserTaskSchema(Schema):
    usertask = fields.Nested(UserTaskSchema)
    project = fields.Nested(ProjectSchema)


# class UserTaskCreateSchema(PlainUserTaskSchema):