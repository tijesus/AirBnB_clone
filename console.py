#!/usr/bin/python3
"""
entry point of the command interpreter using the cmd module
"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State

from models.engine.file_storage import FileStorage
from models import storage
from shlex import split


class HBNBCommand(cmd.Cmd):
    """
    Defines custom command processors for the Airbnb
    project
    """
    prompt = '(hbnb) '

    model_names = {
        'User': User,
        'BaseModel': BaseModel,
        'City': City,
        'Place': Place,
        'State': State,
        'Review': Review,
        'Amenity': Amenity,
    }

    __missing_class_err_msg = '** class name missing **'
    __nonexistent_class_err_msg = '** class doesn\'t exist **'
    __missing_id_err_mesg = '** instance id missing **'
    __nonexistent_id_err_msg = '** no instance found **'
    __missing_attr_err_msg = '** attribute name missing **'
    __nonexistent_attr_err_msg = '** value missing **'

    @staticmethod
    def is_an_object(model_class, id):
        '''
        checks for a model using the model name and id
        key = model class + . + model id
        '''
        key = f"{model_class}.{id}"
        object_dict = storage.all()
        if key in object_dict:
            return True
        return False

    def is_a_modelClass(self, model_class):
        '''checks if model_class is valid'''
        if model_class in self.model_names:
            return True
        return False

    def is_an_attribute(self, model_class, id, attribute):
        '''checks if a model has an atrribute using it's id'''
        model_dict = self.get_model_dict(model_class, id)
        if attribute in model_dict:
            return True
        return False

    @staticmethod
    def get_model_dict(model_class, id):
        '''returns the model's dict representation'''
        key = model_class + '.' + id
        model = storage.all()[key]
        return model

    def do_EOF(self, line):
        '''EOF command to exit the program'''
        print()
        return True

    def do_quit(self, line):
        '''Quit command to exit the program'''
        return True

    def emptyline(self):
        pass

    # Airbnb commands

    def do_create(self, line):
        '''
        Creates a new instance of a Model
        saves it (to the JSON file) and prints the id
        '''
        if line == '':
            print(self.__missing_class_err_msg)
        elif line not in self.model_names:
            print(self.__nonexistent_class_err_msg)
        else:
            instance = self.model_names[line]()
            instance.save()
            print(f"{instance.id}")

    def do_show(self, line):
        """ Prints the string representation of an
        instance based on the class name and id"""

        if line == '':
            print(self.__missing_class_err_msg)
        elif split(line)[0] not in self.model_names:
            print(self.__nonexistent_class_err_msg)
        elif len(split(line)) == 1:
            print(self.__missing_id_err_mesg)
        else:
            found_id = 0
            _model, _model_id = split(line)
            storage_objects = storage.all()

            for key, value in storage_objects.items():
                model, model_id = key.split('.')
                if model_id == _model_id and model == _model:
                    found_id = 1
                    print(value)
                    break

            if not found_id:
                print(self.__nonexistent_id_err_msg)

    def do_destroy(self, line):
        '''deletes an instance'''

        if line == '':
            print(self.__missing_class_err_msg)
        elif split(line)[0] not in self.model_names:
            print(self.__nonexistent_class_err_msg)
        elif len(split(line)) == 1:
            print(self.__missing_id_err_mesg)
        else:
            found_id = 0
            _model, _model_id = split(line)
            storage_objects = storage.all()
            for key, value in storage_objects.items():
                model, model_id = key.split('.')
                if _model_id == model_id and _model == model:
                    found_id = 1
                    break
            if found_id:
                del storage_objects[key]
                storage.save()
            if not found_id:
                print(self.__nonexistent_id_err_msg)

    def do_all(self, line):
        '''Prints all string representation of all instances'''
        str_repr = []
        flag = 0
        all_instances = storage.all()
        for key, value in all_instances.items():
            if line == '':
                str_repr.append(str(value))
                flag = 1
            elif line in self.model_names:
                model, _ = key.split('.')
                if model == line:
                    flag = 1
                    str_repr.append(str(value))
        if flag:
            print(str_repr)
        else:
            print(self.__nonexistent_class_err_msg)

    def do_update(self, line):
        '''Updates an instance based on the class name and id'''

        # class name missing
        if line == '':
            print(self.__missing_class_err_msg)
        # class doesn't exist
        elif not self.is_a_modelClass(split(line)[0]):
            print(self.__nonexistent_class_err_msg)
        # instance id missing
        elif len(split(line)) == 1:
            print(self.__missing_id_err_mesg)
        # no instance found
        elif not self.is_an_object(split(line)[0], split(line)[1]):
            print(self.__nonexistent_id_err_msg)
        # attribute name missing
        elif len(split(line)) == 2:
            print(self.__missing_attr_err_msg)
        # value missing
        elif len(split(line)) == 3:
            print(self.__nonexistent_attr_err_msg)
        else:
            arg_list = split(line)
            arg1 = arg_list[0]
            arg2 = arg_list[1]
            arg3 = arg_list[2]
            arg4 = arg_list[3]
            invalid_attrs = [
                'created_at',
                'updated_at',
                'id'
            ]
            if arg3 in invalid_attrs:
                raise ValueError(
                    f"{arg3} cannot be updated"
                )
            model_instance = self.get_model_dict(arg1, arg2)

            setattr(model_instance, arg3, arg4)
            storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
