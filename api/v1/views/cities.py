#!/usr/bin/python3
"""
This module contains a function to execute console commands
"""

import sys
import cmd
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}


def exec_command(console, the_command):
    """
    This function executes console commands
    Args: console - an instance of a HBNBCommand class
          the_command - a command to execute
    """
    new_dict = None
    if the_command.startswith("create"):
        new_dict = {}
        args = the_command.split()
        if len(args) < 2:
            print("** class name missing **")
            return
        class_name = args[1]
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        if len(args) == 2:
            print("** instance id missing **")
            return
        if len(args) >= 3:
            args.remove(class_name)
            args.remove("create")
            args_str = " ".join(args)
            k_v_pairs = args_str.split(",")
            for pair in k_v_pairs:
                key_value = pair.split("=")
                key = key_value[0]
                value = key_value[1]
                value = value.strip(' "')
                try:
                    value = eval(value)
                except:
                    pass
                new_dict[key] = value
        if not new_dict:
            print("** attribute name missing **")
            return
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        instance = classes[class_name](**new_dict)
        instance.save()
        print(instance.id)


class HBNBCommand(cmd.Cmd):
    """
    This class creates a command line interpreter
    """

    prompt = "(hbnb) "

    def do_EOF(self, line):
        """This function exits the program"""
        return True

    def do_quit(self, line):
        """This function quits the program"""
        return True

    def emptyline(self):
        """This function does nothing"""
        pass

    def do_create(self, line):
        """
        This function creates a new instance of a class
        """
        exec_command(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
