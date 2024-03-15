import random
from django import template


register = template.Library()


@register.filter("randomEntry")
def randomEntry(entries, *args):
  
   
    print("Entries", entries)
    print("Args", args)
    if entries:
        random_entry = random.choice(entries)
        print("Random_Entry", random_entry)
        return random_entry
