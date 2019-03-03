
class URecursive:
    class Matrix:
        @staticmethod
        def extract_elements(matrix, func):
            def check(parent):
                if not type(parent) is list:
                    func(parent)
                    return
                for element in parent:
                    check(element)
            check(matrix)

        @staticmethod
        def on_element(matrix1d):
            def wrap(func):
                def wrapper(*args, **kwargs):
                    for element in matrix1d:
                        func(element, *args, **kwargs)
                return wrapper
            matrix1d = matrix1d
            return wrap
