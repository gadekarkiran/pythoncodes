import click

@click.group()
@click.pass_context
def todo(ctx):
    '''Simple CLI Todo App'''
    ctx.ensure_object(dict)
    try:
        with open('./todo.txt') as f:
            content = f.readlines()
        # First line = latest ID, rest = tasks
        ctx.obj['LATEST'] = int(content[0].strip())
        ctx.obj['TASKS'] = {en.split('|')[0]: en.split('|')[1].strip() for en in content[1:]}
    except FileNotFoundError:
        # Initialize empty file if not present
        ctx.obj['LATEST'] = 1
        ctx.obj['TASKS'] = {}
        with open('./todo.txt', 'w') as f:
            f.write("1\n")

@todo.command()
@click.pass_context
def tasks(ctx):
    '''Display tasks'''
    if ctx.obj['TASKS']:
        click.echo('YOUR TASKS\n**********')
        for i, task in ctx.obj['TASKS'].items():
            click.echo(f'• {task} (ID: {i})')
        click.echo('')
    else:
        click.echo('No tasks yet! Use ADD to add one.\n')

@todo.command()
@click.pass_context
@click.option('-add', '--add_task', prompt='Enter task to add')
def add(ctx, add_task):
    '''Add a task'''
    if add_task:
        ctx.obj['TASKS'][str(ctx.obj['LATEST'])] = add_task
        click.echo(f'Added task "{add_task}" with ID {ctx.obj["LATEST"]}')
        # Write back to todo.txt
        curr_ind = [str(ctx.obj['LATEST'] + 1)]
        tasks = [f"{i}|{t}" for (i, t) in ctx.obj['TASKS'].items()]
        with open('./todo.txt', 'w') as f:
            f.writelines([en + '\n' for en in curr_ind + tasks])

@todo.command()
@click.pass_context
@click.argument('task_id')
def remove(ctx, task_id):
    '''Remove a task by ID'''
    if task_id in ctx.obj['TASKS']:
        removed = ctx.obj['TASKS'].pop(task_id)
        click.echo(f'Removed task {task_id}: {removed}')
        curr_ind = [str(ctx.obj['LATEST'])]
        tasks = [f"{i}|{t}" for (i, t) in ctx.obj['TASKS'].items()]
        with open('./todo.txt', 'w') as f:
            f.writelines([en + '\n' for en in curr_ind + tasks])
    else:
        click.echo(f'No task with ID {task_id}')

@todo.command()
@click.pass_context
@click.argument('task_id')
@click.option('-u', '--update_task', prompt='Enter new task text')
def update(ctx, task_id, update_task):
    '''Update a task by ID'''
    if task_id in ctx.obj['TASKS']:
        ctx.obj['TASKS'][task_id] = update_task
        click.echo(f'Updated task {task_id} → {update_task}')
        curr_ind = [str(ctx.obj['LATEST'])]
        tasks = [f"{i}|{t}" for (i, t) in ctx.obj['TASKS'].items()]
        with open('./todo.txt', 'w') as f:
            f.writelines([en + '\n' for en in curr_ind + tasks])
    else:
        click.echo(f'No task with ID {task_id}')

if __name__ == "__main__":
    todo(obj={})
