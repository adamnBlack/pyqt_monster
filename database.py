from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
import var
import main
import pandas as pd
from pyautogui import alert, password, confirm
import os
import sqlalchemy.sql.default_comparator

db_path = var.base_dir + "/group.db"
Base = declarative_base()
engine = create_engine(
    f'sqlite:///{db_path}', connect_args={'check_same_thread': False})

global logger
logger = var.logging
logger.getLogger("requests").setLevel(var.logging.WARNING)


class Group_A(Base):
    __tablename__ = 'group_a'
    id = Column(Integer, primary_key=True)
    FIRSTFROMNAME = Column(String)
    LASTFROMNAME = Column(String)
    EMAIL = Column(String)
    EMAIL_PASS = Column(String)
    PROXY_PORT = Column(String)
    PROXY_USER = Column(String)
    PROXY_PASS = Column(String)


class Group_B(Base):
    __tablename__ = 'group_b'
    id = Column(Integer, primary_key=True)
    FIRSTFROMNAME = Column(String)
    LASTFROMNAME = Column(String)
    EMAIL = Column(String)
    EMAIL_PASS = Column(String)
    PROXY_PORT = Column(String)
    PROXY_USER = Column(String)
    PROXY_PASS = Column(String)


class Targets(Base):
    __tablename__ = 'targets'
    id = Column(Integer, primary_key=True)
    one = Column(String)
    two = Column(String)
    three = Column(String)
    four = Column(String)
    five = Column(String)
    six = Column(String)
    TONAME = Column(String)
    EMAIL = Column(String)


Base.metadata.create_all(engine)


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


class Database:
    def __init__(self):
        """initialize the class """

        global logger
        self.logger = logger
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.table = {
            "group_a": Group_A,
            "group_b": Group_B,
            "targets": Targets
        }

    def remove(self, table=None, id=None):
        """remove row from table by id and this method expects
        two arguments table and id of that row"""

        try:
            if table != None and id != None:
                objects = self.session.query(self.table[table]).get(int(id))

                if objects:
                    self.session.delete(objects)
                    self.session.commit()
                    self.logger.info(f"Deleted id - {id}")
                    return True
            else:
                print("please provide table and id")
                return False

        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error at Database.remove() - {e}")
            return False


def db_update_row(row):
    try:
        session = get_session()

        if main.GUI.radioButton_db_groupa.isChecked():
            objects = session.query(Group_A).get(int(row['ID']))
            objects.FIRSTFROMNAME = row["FIRSTFROMNAME"]
            objects.LASTFROMNAME = row["LASTFROMNAME"]
            objects.EMAIL = row["EMAIL"]
            objects.EMAIL_PASS = row["EMAIL_PASS"]
            objects.PROXY_PORT = row["PROXY:PORT"]
            objects.PROXY_USER = row["PROXY_USER"]
            objects.PROXY_PASS = row["PROXY_PASS"]

        elif main.GUI.radioButton_db_groupb.isChecked():
            objects = session.query(Group_B).get(int(row['ID']))
            objects.FIRSTFROMNAME = row["FIRSTFROMNAME"]
            objects.LASTFROMNAME = row["LASTFROMNAME"]
            objects.EMAIL = row["EMAIL"]
            objects.EMAIL_PASS = row["EMAIL_PASS"]
            objects.PROXY_PORT = row["PROXY:PORT"]
            objects.PROXY_USER = row["PROXY_USER"]
            objects.PROXY_PASS = row["PROXY_PASS"]

        else:
            objects = session.query(Targets).get(int(row['ID']))
            objects.one = row["1"]
            objects.two = row["2"]
            objects.three = row["3"]
            objects.four = row["4"]
            objects.five = row["5"]
            objects.six = row["6"]
            objects.TONAME = row["TONAME"]
            objects.EMAIL = row["EMAIL"]

        session.commit()
        print("db updated")
        return True

    except Exception as e:
        session.rollback()
        print(f"Error at var.db_update_row : {e}")
        global logger
        logger.error(f"Error at db_update_row - {e}")
        return False


def db_remove_row(id):
    try:
        session = get_session()

        if main.GUI.radioButton_db_groupa.isChecked():
            objects = session.query(Group_A).get(id)
        elif main.GUI.radioButton_db_groupb.isChecked():
            objects = session.query(Group_B).get(id)
        else:
            objects = session.query(Targets).get(id)

        if objects:
            session.delete(objects)
            session.commit()
            print("db updated")
            return True
        else:
            return False

    except Exception as e:
        session.rollback()
        print(f"Error at var.db_remove_row : {e}")
        global logger
        logger.error(f"Error at var.db_remove_row - {e}")
        return False


def db_remove_rows(ids):
    try:
        session = get_session()
        for id in ids:
            if main.GUI.radioButton_db_groupa.isChecked():
                objects = session.query(Group_A).get(id)
            elif main.GUI.radioButton_db_groupb.isChecked():
                objects = session.query(Group_B).get(id)
            else:
                objects = session.query(Targets).get(id)

            if objects:
                session.delete(objects)

        session.commit()

        print("db updated")

    except Exception as e:
        session.rollback()
        print(f"Error at var.db_remove_rows : {e}")
        global logger
        logger.error(f"Error at var.db_remove_rows - {e}")


def db_insert_row():
    try:
        session = get_session()

        if main.GUI.radioButton_db_groupa.isChecked():
            objects = Group_A(
                FIRSTFROMNAME="",
                LASTFROMNAME="",
                EMAIL="",
                EMAIL_PASS="",
                PROXY_PORT="",
                PROXY_USER="",
                PROXY_PASS=""
            )
        elif main.GUI.radioButton_db_groupb.isChecked():
            objects = Group_B(
                FIRSTFROMNAME="",
                LASTFROMNAME="",
                EMAIL="",
                EMAIL_PASS="",
                PROXY_PORT="",
                PROXY_USER="",
                PROXY_PASS=""
            )
        else:
            objects = Targets(
                one="",
                two="",
                three="",
                four="",
                five="",
                six="",
                TONAME="",
                EMAIL=""
            )

        session.add(objects)
        session.commit()
        print("db updated")
        return True, objects.id

    except Exception as e:
        session.rollback()
        print(f"Error at var.db_insert_row : {e}")
        global logger
        logger.error(f"Error at var.db_insert_row - {e}")
        return False, None


def file_to_db():
    session = get_session()
    logger.error(f"File loading Config: {var.db_file_loading_config}")

    group_header = ['FIRSTFROMNAME', 'LASTFROMNAME', 'EMAIL',
                    'EMAIL_PASS', 'PROXY:PORT', 'PROXY_USER', 'PROXY_PASS']

    target_header = ['1', '2', '3', '4', '5', '6', 'TONAME', 'EMAIL']

    try:
        if var.db_file_loading_config['group_a']:
            clear_table(group_a=True)

            if os.path.exists(var.base_dir + '/group_a.xlsx'):
                group_a = pd.read_excel(var.base_dir + '/group_a.xlsx',
                                        engine='openpyxl', sheet_name="group_a")
                group_a = group_a[group_header]

                if list(group_a.keys()) == group_header:

                    group_a.fillna(" ", inplace=True)
                    group_a = group_a.astype(str)
                    group_a = group_a.loc[group_a['PROXY:PORT'] != " "]

                    if len(group_a) > 0:
                        objects = [Group_A(
                            FIRSTFROMNAME=row['FIRSTFROMNAME'],
                            LASTFROMNAME=row['LASTFROMNAME'],
                            EMAIL=row['EMAIL'],
                            EMAIL_PASS=row['EMAIL_PASS'],
                            PROXY_PORT=row['PROXY:PORT'],
                            PROXY_USER=row['PROXY_USER'],
                            PROXY_PASS=row['PROXY_PASS']

                        ) for index, row in group_a.iterrows()]

                        session.add_all(objects)
                    else:
                        objects = Group_A(
                            id=1,
                            FIRSTFROMNAME="",
                            LASTFROMNAME="",
                            EMAIL="",
                            EMAIL_PASS="",
                            PROXY_PORT="",
                            PROXY_USER="",
                            PROXY_PASS=""
                        )
                        session.add(objects)

                    session.commit()
                else:
                    raise Exception("Header's not matching on Group A.")
            else:
                raise Exception("Group A file not found.")
        else:
            print("skipping Group A")
    except Exception as e:
        logger.error(f"Error while loading Group A: {e}")
        dummy_data_db(group_a=True, group_b=False, target=False)
        return False, e

    try:
        if var.db_file_loading_config['group_b']:
            clear_table(group_b=True)

            if os.path.exists(var.base_dir + '/group_b.xlsx'):
                group_b = pd.read_excel(var.base_dir + '/group_b.xlsx',
                                        engine='openpyxl', sheet_name="group_b")
                group_b = group_b[group_header]

                if list(group_b.keys()) == group_header:

                    group_b.fillna(" ", inplace=True)
                    group_b = group_b.astype(str)
                    group_b = group_b.loc[group_b['PROXY:PORT'] != " "]

                    if len(group_b) > 0:
                        objects = [Group_B(
                            FIRSTFROMNAME=row['FIRSTFROMNAME'],
                            LASTFROMNAME=row['LASTFROMNAME'],
                            EMAIL=row['EMAIL'],
                            EMAIL_PASS=row['EMAIL_PASS'],
                            PROXY_PORT=row['PROXY:PORT'],
                            PROXY_USER=row['PROXY_USER'],
                            PROXY_PASS=row['PROXY_PASS']

                        ) for index, row in group_b.iterrows()]

                        session.add_all(objects)
                    else:
                        objects = Group_B(
                            id=1,
                            FIRSTFROMNAME="",
                            LASTFROMNAME="",
                            EMAIL="",
                            EMAIL_PASS="",
                            PROXY_PORT="",
                            PROXY_USER="",
                            PROXY_PASS=""
                        )
                        session.add(objects)

                    session.commit()
                else:
                    raise Exception("Header's not matching on Group B.")
            else:
                raise Exception("Group B file not found.")
        else:
            print("skipping Group B")
    except Exception as e:
        logger.error(f"Error while loading Group B: {e}")
        dummy_data_db(group_a=False, group_b=True, target=False)
        return False, e

    try:
        if var.db_file_loading_config['target']:
            clear_table(target=True)

            if os.path.exists(var.base_dir + '/target.xlsx'):
                target = pd.read_excel(var.base_dir + '/target.xlsx',
                                       engine='openpyxl', sheet_name="target")

                target.columns = target.columns.astype(str)
                target = target[target_header]

                if list(target.keys()) == target_header:

                    target.fillna(" ", inplace=True)
                    target = target.astype(str)
                    target = target.loc[target['EMAIL'] != " "]

                    if len(var.target_blacklist) > 0:
                        target = target[~target['EMAIL'].str.lower(
                        ).str.contains("|".join(var.target_blacklist))]

                    if len(target) > 0:
                        objects = [Targets(
                            one=row['1'],
                            two=row['2'],
                            three=row['3'],
                            four=row['4'],
                            five=row['5'],
                            six=row['6'],
                            TONAME=row['TONAME'],
                            EMAIL=row['EMAIL']

                        ) for index, row in target.iterrows()]

                        session.add_all(objects)

                    else:
                        objects = Targets(
                            id=1,
                            one="",
                            two="",
                            three="",
                            four="",
                            five="",
                            six="",
                            TONAME="",
                            EMAIL=""
                        )
                        session.add(objects)

                    session.commit()
                else:
                    raise Exception("Header's not matching on Target.")
            else:
                raise Exception("Target file not found.")
        else:
            print("skipping Target")
    except Exception as e:
        logger.error(f"Error while loading Target: {e}")
        dummy_data_db(group_a=False, group_b=False, target=True)
        return False, e

    return True, None


def dummy_data_db(group_a=True, group_b=True, target=True):
    session = get_session()
    if group_a:
        objects = Group_A(
            id=1,
            FIRSTFROMNAME="",
            LASTFROMNAME="",
            EMAIL="",
            EMAIL_PASS="",
            PROXY_PORT="",
            PROXY_USER="",
            PROXY_PASS=""
        )
        session.add(objects)

    if group_b:
        objects = Group_B(
            id=1,
            FIRSTFROMNAME="",
            LASTFROMNAME="",
            EMAIL="",
            EMAIL_PASS="",
            PROXY_PORT="",
            PROXY_USER="",
            PROXY_PASS=""
        )
        session.add(objects)

    if target:
        objects = Targets(
            id=1,
            one="",
            two="",
            three="",
            four="",
            five="",
            six="",
            TONAME="",
            EMAIL=""
        )
        session.add(objects)

    session.commit()


def pandas_to_db():
    try:
        session = get_session()
        objects = [Group_A(
            FIRSTFROMNAME=row['FIRSTFROMNAME'],
            LASTFROMNAME=row['LASTFROMNAME'],
            EMAIL=row['EMAIL'],
            EMAIL_PASS=row['EMAIL_PASS'],
            PROXY_PORT=row['PROXY:PORT'],
            PROXY_USER=row['PROXY_USER'],
            PROXY_PASS=row['PROXY_PASS']

        ) for index, row in var.group_a.iterrows()]

        session.add_all(objects)

        objects = [Group_B(
            FIRSTFROMNAME=row['FIRSTFROMNAME'],
            LASTFROMNAME=row['LASTFROMNAME'],
            EMAIL=row['EMAIL'],
            EMAIL_PASS=row['EMAIL_PASS'],
            PROXY_PORT=row['PROXY:PORT'],
            PROXY_USER=row['PROXY_USER'],
            PROXY_PASS=row['PROXY_PASS']

        ) for index, row in var.group_b.iterrows()]

        session.add_all(objects)

        objects = [Targets(
            one=row['1'],
            two=row['2'],
            three=row['3'],
            four=row['4'],
            five=row['5'],
            six=row['6'],
            TONAME=row['TONAME'],
            EMAIL=row['EMAIL']

        ) for index, row in var.target.iterrows()]

        session.add_all(objects)
        print("Pandas to DB done!")
    except Exception as e:
        print(f"Error at var.pandas_to_db : {e}")
        global logger
        logger.error(f"Error at var.pandas_to_db - {e}")


def db_to_pandas():
    session = get_session()

    results = session.query(Group_A).all()

    group_a_list = [{
                        'ID': item.id,
                        'FIRSTFROMNAME': item.FIRSTFROMNAME,
                        'LASTFROMNAME': item.LASTFROMNAME,
                        'EMAIL': item.EMAIL,
                        'EMAIL_PASS': item.EMAIL_PASS,
                        'PROXY:PORT': item.PROXY_PORT,
                        'PROXY_USER': item.PROXY_USER,
                        'PROXY_PASS': item.PROXY_PASS
                    }.copy() for item in results]

    var.group_a = pd.DataFrame(group_a_list)

    results = session.query(Group_B).all()

    group_b_list = [{
                        'ID': item.id,
                        'FIRSTFROMNAME': item.FIRSTFROMNAME,
                        'LASTFROMNAME': item.LASTFROMNAME,
                        'EMAIL': item.EMAIL,
                        'EMAIL_PASS': item.EMAIL_PASS,
                        'PROXY:PORT': item.PROXY_PORT,
                        'PROXY_USER': item.PROXY_USER,
                        'PROXY_PASS': item.PROXY_PASS
                    }.copy() for item in results]

    var.group_b = pd.DataFrame(group_b_list)

    results = session.query(Targets).all()

    if len(results) > 0:
        targets_list = [{
                            'ID': item.id,
                            '1': item.one,
                            '2': item.two,
                            '3': item.three,
                            '4': item.four,
                            '5': item.five,
                            '6': item.six,
                            'TONAME': item.TONAME,
                            'EMAIL': item.EMAIL
                        }.copy() for item in results]

    else:
        dummy_data_db(group_a=False, group_b=False, target=True)
        results = session.query(Targets).all()
        targets_list = [{
                            'ID': item.id,
                            '1': item.one,
                            '2': item.two,
                            '3': item.three,
                            '4': item.four,
                            '5': item.five,
                            '6': item.six,
                            'TONAME': item.TONAME,
                            'EMAIL': item.EMAIL
                        }.copy() for item in results]

    var.target = pd.DataFrame(targets_list)
    print(var.group_a.head(5))
    print(var.group_b.head(5))
    print(var.target.head(5))


def clear_table(group_a=None, group_b=None, target=None):
    try:
        session = get_session()

        if group_a:
            session.query(Group_A).delete()

        if group_b:
            session.query(Group_B).delete()

        if target:
            session.query(Targets).delete()

        session.commit()

    except Exception as e:
        session.rollback()
        print("Exeception occured at clear db table : {}".format(e))
        global logger
        logger.error(f"Error at clear db table - {e}")


def load_db():
    try:
        result, error = file_to_db()
        db_to_pandas()
        var.command_q.put("self.update_db_table()")
        if result:
            alert(text="Database Loaded Successfully",
                  title='Alert', button='OK')
        else:
            raise error

    except Exception as e:
        print("Exeception occured at db loading : {}".format(e))
        alert(text="Exeception occured at db loading : {}".format(
            e), title='Alert', button='OK')


def startup_load_db(parent=None):
    try:
        session = get_session()
        group_a = True if session.query(Group_A).first() == None else False
        group_b = True if session.query(Group_B).first() == None else False
        target = True if session.query(Targets).first() == None else False

        dummy_data_db(group_a=group_a, group_b=group_b, target=target)

        db_to_pandas()
        var.command_q.put("self.update_db_table()")

    except Exception as e:
        print("Exeception occured at startup_db loading : {}".format(e))
        alert(text="Exeception occured at startup_db loading : {}".format(
            e), title='Alert', button='OK')
