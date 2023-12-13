from django.core.management.base import BaseCommand
from contents.models import Category


class Command(BaseCommand):
    help = "CRUD category"

    def add_arguments(self, parser):
        parser.add_argument("--CRUD", type=str, help="CRUD actions for category model")
        parser.add_argument("--name", type=str, help="Name of the category")
        parser.add_argument("--parent", type=str, help="Parent category")
        parser.add_argument("--new_name", type=str, help="New name of the category")
        

    def handle(self, *args, **kwargs) -> str | None:
        crud_action = kwargs["CRUD"]

        if crud_action == "c":
            name = kwargs["name"]
            parent_category_name = kwargs.get("parent", None)

            parent_category = None
            if parent_category_name:
                parent_category = Category.objects.get(name=parent_category_name)

            new_category = Category(name=name, parent=parent_category)
            new_category.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created category: {name}")
            )

        elif crud_action == "r":
            categories = Category.objects.all()
            for category in categories:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Category: {category.name}, Parent: {category.parent}"
                    )
                )

        elif crud_action == "u":
            name = kwargs["name"]
            new_name = kwargs.get("new_name", None)
            parent_category_name = kwargs.get("parent", None)

            category = Category.objects.get(name=name)

            if new_name:
                category.name = new_name
            if parent_category_name:
                parent_category = Category.objects.get(name=parent_category_name)
                category.parent = parent_category

            category.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully updated category: {name}")
            )

        elif crud_action == "d":
            name = kwargs["name"]
            category = Category.objects.get(name=name)
            category.delete()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully deleted category: {name}")
            )

        else:
            self.stdout.write(self.style.ERROR("Invalid action"))
