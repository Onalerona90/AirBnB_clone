#!/usr/bin/python3
import cmd
from models import storage
from models.base_model import classes
import re
import json

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Exit the program when 'EOF' (Ctrl+D) is entered"""
        print()
        return True

    def do_create(self, arg):
        """Create command to create a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        elif args[0] not in classes:
            print("** class doesn't exist **")
            return
        new_instance = classes[args[0]]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Show command to display the details of a specific instance"""
        args = arg.split()
        if len(args) < 2:
            print("** instance id missing **")
            return
        elif args[0] not in classes:
            print("** class doesn't exist **")
            return
        instances = storage.all()
        instance_key = "{}.{}".format(args[0], args[1])
        if instance_key not in instances:
            print("** no instance found **")
            return
        print(instances[instance_key])

    def do_destroy(self, arg):
        """Destroy command to delete a specific instance"""
        args = arg.split()
        if len(args) < 2:
            print("** instance id missing **")
            return
        elif args[0] not in classes:
            print("** class doesn't exist **")
            return
        instances = storage.all()
        instance_key = "{}.{}".format(args[0], args[1])
        if instance_key not in instances:
            print("** no instance found **")
            return
        del instances[instance_key]
        storage.save()

    def do_all(self, arg):
        """All command to display all instances of a class"""
        args = arg.split()
        if len(args) == 0 or args[0] not in classes:
            print("** class doesn't exist **")
            return
        instances = storage.all()
        instances_list = [str(instance) for key, instance in instances.items() if re.match(args[0], key)]
        print(instances_list)

    def do_update(self, arg):
        """Update command to update the attributes of a specific instance"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        elif args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instances = storage.all()
        instance_key = "{}.{}".format(args[0], args[1])
        if instance_key not in instances:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        try:
            setattr(instances[instance_key], args[2], eval(args[3]))
            storage.save()
        except:
            pass

    def default(self, line):
        """Default command for handling unknown commands"""
        command, arg = line.split('.', 1)
        if command in ['all', 'count']:
            self.do_all(arg.strip()) if command == 'all' else self.do_count(arg.strip())
        elif command in ['show', 'destroy']:
            self.do_show(arg.strip()) if command == 'show' else self.do_destroy(arg.strip())
        elif command == 'update':
            self.do_update(arg.strip())
        else:
            print("*** Unknown syntax: {}".format(line))
            return

    def do_count(self, class_name):
        """Count command to count the instances of a class"""
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        instances = storage.all()
        count = sum(1 for key in instances.keys() if re.match(class_name, key))
        print(count)

    def emptyline(self):
        """Empty line handler"""
        pass

if __name__ == "__main__":
    HBNBCommand().cmdloop()
