import numpy as np

class PatternLibrary:
    @staticmethod
    def dot(x, y):
        
        return (np.sin(x) + np.cos(y)) / 2.0

    @staticmethod
    def line(x, y):
        
        return np.sin(x)

    @staticmethod
    def square(x, y):
        
        return np.sin(x) * np.cos(y)

    @staticmethod
    def cross(x, y):
       
        return np.maximum(np.sin(x), np.cos(y))

    @staticmethod
    def diamond(x, y):
        
        return np.abs(np.sin(x)) + np.abs(np.cos(y)) - 1.0

    @staticmethod
    def euclidean(x, y):
        
        return np.sqrt(np.sin(x) ** 2 + np.cos(y) ** 2)

    @staticmethod
    def ellipse(x, y):
        
        return np.sqrt(np.sin(x) ** 2 + (np.cos(y) * 0.5) ** 2)
