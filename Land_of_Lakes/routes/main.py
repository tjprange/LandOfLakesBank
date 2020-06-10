from flask import Blueprint, render_template
from ..forms import TablesForm, ConnectAdvisorForm, SearchForm
from ..db_connector.db_connector import connect_to_database, execute_query

main = Blueprint('main', __name__)


# Homepage route
@main.route('/')
def index():

    return render_template('index.html')


# This route will connect an existing financial advisor to an existing client
@main.route('/connect_advisor', methods=['GET', 'POST'])
def connect_advisor():
    db_connection = connect_to_database()
    form = ConnectAdvisorForm()
    if form.validate_on_submit():
        client_id = form.client_id.data
        advisor_id = form.advisor_id.data
        clients_advisors_query = (f"INSERT INTO `clients_advisors`\
                                    (`client_id`, `advisor_id`)\
                                VALUES ('{client_id}', '{advisor_id}');")

        execute_query(db_connection, clients_advisors_query)

    return render_template('connect_advisor.html', form=form)


# This route will search the database for a client with the specified form data.
# If the string is found in the database, it will be rendered into the html page.
@main.route('/search_database', methods=['GET', 'POST'])
def search_database():
    db_connection = connect_to_database()
    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.searched_parameter.data
        print("searching for: " + search_term)

        query = (f"SELECT * FROM `clients`\
                 WHERE last_name LIKE '{search_term}%';")

        rows = execute_query(db_connection, query, None).fetchall()

        return render_template('search_database.html', form=form, rows=rows)

    return render_template('search_database.html', form=form)

# This route will display data from each one of our tables. The user is provided a drop-
# down menu in which to choose the table data they wish to view. The resulting data from the
# cooresponding table is then rendered to the user.
@main.route('/view_tables', methods=['GET', 'POST'])
def view_tables():
    db_connection = connect_to_database()

    form = TablesForm()

    if form.validate_on_submit():
        # Display clients table data
        if form.tables.data == 'clients':
            query = ("SELECT\
                        `client_id` as 'Client ID',\
                        `ssn` as 'Social Security Number',\
                    CONCAT(`first_name`, ' ', `last_name`) as 'Client Name',\
                        `email` as 'Email',\
                        `address_id` as 'Address ID'\
                     FROM\
                        `clients`;")

            rows = execute_query(db_connection, query).fetchall()

            return render_template('view_clients.html', form=form, rows=rows)
        # Display accounts table data
        elif form.tables.data == 'accounts':
            query = ("SELECT\
                        `account_id` as 'Account Number',\
                        `balance` as 'Account Balance'\
                     FROM\
                        `accounts`;")

            rows = execute_query(db_connection, query).fetchall()

            return render_template('view_accounts.html', form=form, rows=rows)
        # Display clients_advisors table data
        elif form.tables.data == 'clients_advisors':
            query = ("SELECT\
                        `client_advisor_id` as 'Client Advisor ID',\
                        clients.client_id as 'Client ID',\
                        clients.first_name as 'C First',\
                        clients.last_name as 'C Last',\
                        financial_advisors.advisor_id as 'Advisor ID',\
                        financial_advisors.first_name as 'A First',\
                        financial_advisors.last_name as 'A Last'\
                    FROM\
                        `clients_advisors`\
                        INNER JOIN clients\
                        ON clients.client_id=clients_advisors.client_id\
                        INNER JOIN financial_advisors\
                        ON financial_advisors.advisor_id\
                           =clients_advisors.advisor_id;")

            rows = execute_query(db_connection, query).fetchall()

            return render_template('view_clients_advisors.html',
                                   form=form,
                                   rows=rows)

        # Display clients_accounts table data
        elif form.tables.data == 'clients_accounts':
            query = ("SELECT\
                            `client_account_id` as 'Client Account ID',\
                            clients.first_name as 'First Name',\
                            clients.last_name as 'Last Name',\
                            clients.client_id as 'Client ID',\
                            accounts.account_id as 'Account ID'\
                            FROM\
                            `clients_accounts`\
                            INNER JOIN clients\
                            ON clients.client_id=clients_accounts.client_id\
                            INNER JOIN accounts\
                            ON accounts.account_id\
                            =clients_accounts.account_id;")

            rows = execute_query(db_connection, query).fetchall()

            return render_template('view_clients_accounts.html',
                                   form=form,
                                   rows=rows)

        # Display addresses table data
        elif form.tables.data == 'addresses':
            query = ("SELECT\
                            `address_id` as 'Address ID',\
                            `city` as 'City',\
                            `state` as 'State',\
                            `house_number` as 'House Number',\
                            `zip_code` as 'Zip Code'\
                    FROM\
                            `addresses`;")

            rows = execute_query(db_connection, query).fetchall()

            return render_template('view_addresses.html', form=form, rows=rows)

        # Display financial_advisors table data
        elif form.tables.data == 'financial_advisors':

            query = ("SELECT\
                        `advisor_id` as 'Advisor ID',\
                        `area_of_expertise` as 'Area of Expertise',\
                        `first_name` as 'First Name',\
                        `last_name` as 'Last Name'\
                    FROM\
                        `financial_advisors`;")

            rows = execute_query(db_connection, query).fetchall()

            return render_template('view_financial_advisors.html', form=form, rows=rows)

    return render_template('view_tables.html', form=form)
