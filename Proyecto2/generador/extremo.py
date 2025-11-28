class ExtremeGenerator:

    def __init__(self, derivator):
        self.derivator = derivator

    def long_expression(self, repetitions=10, max_length=None):
        expr = ""
        for _ in range(repetitions):
            expr += self.derivator.generate()

            if max_length and len(expr) >= max_length:
                return expr[:max_length]

        return expr

    def deep_expression(self, depth):
        old_depth = self.derivator.max_depth
        self.derivator.max_depth = depth
        expr = self.derivator.generate()
        self.derivator.max_depth = old_depth
        return expr
