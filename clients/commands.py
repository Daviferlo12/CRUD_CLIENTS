import click
from clients.services import ClientService
from clients.models import Client
from tabulate import tabulate
 

@click.group()
def clients():
    """Manages the clients lifecycle"""
    pass



@clients.command()
@click.option('-n', '--name',
              type=str,
              prompt=True,
              help='The client name')
@click.option('-e', '--email',
              type=str,
              prompt=True,
              help='The client mail')
@click.option('-c', '--company',
              type=str,
              prompt=True,
              help='The client company')
@click.option('-p', '--position',
              type=str,
              prompt=True,
              help='The client position')
@click.pass_context
def create(ctx, name, email, company, position):
    """Creates a new client"""
    client = Client(name, email, company, position)
    client_service= ClientService(ctx.obj['clients_table'])
    client_service.create_client(client)


    

@clients.command()
@click.pass_context
def list(ctx):
    """List all clients"""
    client_service = ClientService(ctx.obj['clients_table'])
    clients_list = client_service.list_clients()
    
    headers = [field.capitalize() for field in Client.schema()]
    table = []
    
    for client in clients_list:
        table.append([
            client['uid'],
            client['name'],
            client['email'],
            client['company'],
            client['position'],
        ])
        
    
    click.echo(tabulate(table, headers))
        


@clients.command()
@click.argument('client_uid',
                type=str)
@click.pass_context
def update(ctx, client_uid):
    """Update a client"""
    client_service = ClientService(ctx.obj['clients_table'])
    
    client = [client for client in client_service.list_clients() if client['uid'] == client_uid]
    
    if client:
        client = _update_client_flow(Client(**client[0]))
        client_service.update_client(client)
        
        click.echo("[*] Client updated")
    else:
        click.echo("[*] Client not found")


def _update_client_flow(client):
    click.echo('Leave empty if you don\'t wanna modify the value')
    
    client.name = click.prompt('New name', type=str, default=client.name)
    client.email = click.prompt('New email', type=str, default=client.email)
    client.company = click.prompt('New company', type=str, default=client.company)
    client.position = click.prompt('New position', type=str, default=client.position)
    
    return client
    

    
@clients.command()
@click.argument('client_uid',
                type=str)
@click.pass_context
def delete(ctx, client_uid):
    """Delete a cliente"""
    
    client_service = ClientService(ctx.obj['clients_table'])
    
    client = [client for client in client_service.list_clients() if client['uid'] == client_uid]

    # print(f'CLIENTE : {type(Client(**client[0]))}')
    
    if client:
        client_service.delete_client(Client(**client[0]))
        click.echo("[*] Client deleted")
    else:
        click.echo("[*] Client not found")


all = clients
