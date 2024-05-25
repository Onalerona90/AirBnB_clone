#!/usr/bin/python3
'''Command Line Interpreter'''
import cmd
import sys

from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_EOF(self, line):
        """
        Exit the program when 'EOF' (Ctrl+D) is entered
        """
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def validate_class_existence(self, class_name):
        """
        Validate if a class exists in the storage
        """
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return False
        return True

    def validate_instance_existence(self, class_name, instance_id):
        """
        Validate if an instance exists in the storage
        """
        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print("** no instance found **")
            return False
        return True

    def do_create(self, line):
        """
        Usage: create <class name>
        Function: Creates an instance of the class
        """
        if not line:
            print("** class name missing **")
            return
        class_name = line.strip()
        if self.validate_class_existence(class_name):
            obj_instance = storage.classes()[class_name]()
            obj_instance.save()
            print(obj_instance.id)

    def do_show(self, line):
        """
        Usage: show <class name> <id>
        Function: Shows the instance details of the class
        """
        args = line.split()
        if len(args) != 2:
            print("** instance id missing **")
            return

        class_name, instance_id = args
        if (self.validate_class_existence(class_name) and
                self.validate_instance_existence(class_name, instance_id)):
            instance_dict = storage.all()[f"{class_name}.{instance_id}"]
            print(instance_dict)

    def do_destroy(self, line):
        """
        Usage: destroy <class name> <id>
        Function: Deletes the instance of the class
        """
        args = line.split()
        if len(args) != 2:
            print("** class name missing **")
            return

        class_name, instance_id = args
        if (self.validate_class_existence(class_name) and
                self.validate_instance_existence(class_name, instance_id)):
            del storage.all()[f"{class_name}.{instance_id}"]
            storage.save()

    def do_all(self, line):
        """
        Usage: all [class name]
        Function: Prints the string representation of all instances
        """
        class_name = line.strip()
        if not class_name:
            print("** class name missing **")
            return

        if not self.validate_class_existence(class_name):
            return

        instance_list = [str(obj) for obj in storage.classes()[class_name].all()]
        print(instance_list)

    def update_instance(self, class_name, instance_id, attribute, value):
        """
        Update the dictionary
        """
        instance_dict = storage.all()[f"{class_name}.{instance_id}"]
        value = value.strip('"')
        setattr(instance_dict, attribute, value)
        new_instance_dict = {attribute: value}
        new_instance_dict.update(instance_dict.__dict__)

        # Update the instance with the new dictionary
        instance_dict.__dict__ = new_instance_dict
        storage.save()

    def do_update(self, line):
        """
        Usage: update <class name> <id> <attribute> <value>
        Function: Updates the instance of the class
        """
        args = line.split()
        if len(args) != 4:
            print("Usage: update <class name> <id> <attribute> <value>")
            return

        class_name, instance_id, attribute, value = args
        self.update_instance(class_name, instance_id, attribute, value)

    def do_count(self, line):
        """
        Usage: count <class name>
        Function: Counts all the instances of the class
        """
        class_name = line.strip()
        count = sum(
            1 for key in storage.all().keys()
            if not class_name or key.startswith(class_name + ".")
        )
        print(count)

    def emptyline(self):
        pass

    def precmd(self, line):
        """
        Make the app work non-interactively
        """
        if not sys.stdin.isatty():
            print()
        return cmd.Cmd.precmd(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
