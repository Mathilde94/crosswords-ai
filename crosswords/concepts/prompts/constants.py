EXTRACT_CONCEPTS = """Below is an instruction that describes a task, paired with an input that provides further context.
Write a response that appropriately completes the request.

Instruction: 
Given a passage of a content, extract main learning concepts from the content below. 
Return between 2 and 5 concepts, in a comma separated list. 

Example:
title: Python for intermediate
section: Object Oriented Programming
extract: Hello, today we are going to learn about inheritance, parents classes setting attributes for children classes, composition, creating new objects, classes vs instances, and super methods. 
concepts: inheritance, super, composition, class, attributes

Your turn:
title: {title}
section: {section}
extract: {extract}
concepts:"""
