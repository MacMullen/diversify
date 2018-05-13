import unittest
import numpy as np
import numpy.testing as tst
import splearn as spl


class TestSp(unittest.TestCase):

    def setUp(self):
        self.data = np.array([[0, 0],
                              [0, 1],
                              [1, 0],
                              [1, 1]], dtype='float64')
        self.target = np.array([[0, 0],
                                [1, 0],
                                [1, 0],
                                [0, 1]], dtype='float64')

    def test_constructor(self):
        randomlayers = np.random.randint(1, 6, 5)

        def test_numpy(expected, value):
            expected.insert(0, np.zeros(shape=(2, 1)))
            expected.append(np.zeros(shape=(2, 1)))
            for exp, t in zip(expected, value):
                self.assertTrue(np.array_equal(exp, t))

        # Teste construtor por valores das camadas
        neural1 = spl.MLP(9, 5).fit(self.data, self.target)
        test_numpy([np.zeros(shape=(9, 1)) for _ in range(5)], neural1._network)
        # Teste construtor por iteravel
        neural2 = spl.MLP(randomlayers).fit(self.data, self.target)
        test_numpy([np.zeros(shape=(value, 1)) for value in randomlayers], neural2._network)
        # Teste construtor por inteiro
        neural3 = spl.MLP(9).fit(self.data, self.target)
        test_numpy([np.zeros(shape=(9, 1)) for _ in range(9)], neural3._network)
        # Teste construtor por pacote
        neural4 = spl.MLP(*randomlayers).fit(self.data, self.target)
        test_numpy([np.zeros(shape=(value, 1)) for value in randomlayers], neural4._network)

        # Testando construtores errados
        with self.assertRaises(TypeError):
            wronglayers = np.random.rand(3)
            print("Shape wronglayers: {0}".format(wronglayers.shape))
            # Teste construtor por float
            spl.MLP(3.7)
            # Teste construtor por string
            spl.MLP("marcelinho")
            # Teste construtor por tipo aleatorio
            spl.MLP(int)
            # Teste construtor por array de floats
            spl.MLP(wronglayers)
            # Teste construtor por sequencia de floats
            spl.MLP(*wronglayers)

    def test_fitting(self):
        ml = spl.MLP([2])
        ml.fit(self.data, self.target)
        for layer in ml._network:
            print(layer)

        npnp = self.data
        arrarr = npnp.tolist()
        arrnp = [sample for sample in self.data]

        spl.MLP(2, 1).fit(npnp, self.target)
        #spl.MLP(2, 1).fit(arrarr, self.target)
        #spl.MLP(2, 1).fit(arrnp, self.target)

    def test_foward(self):
        weight1 = np.array([[0.3, 0.8, 0.7],
                            [0.5, 0.6, 0.2]])
        weight2 = np.array([[0.1, 0.4, 0.9],
                            [0.5, 0.3, 0.6]])
        first = np.array([[0.0, 0.0]])
        target = np.array([[0.0, 0.0]])
        testinput = np.array([0.0, 0.0])

        neural = spl.MLP(2, 1).fit(first, target)
        neural._weights[0] = weight1
        neural._weights[1] = weight2
        testtarget = np.array([0.33, 0.425]).reshape(2, 1)
        tst.assert_almost_equal(neural._forward(testinput), testtarget, decimal=2)

    def test_predict(self):
        neural = spl.MLP(2, 1).fit(self.data, self.target)
        result = neural.predict(np.array([[0, 1]]))
        print(result)

    def test_back(self):
        weight1 = np.array([[0.3, 0.8, 0.7],
                            [0.5, 0.6, 0.2]])
        weight2 = np.array([[0.1, 0.4, 0.9],
                            [0.5, 0.3, 0.6]])
        first = np.array([[0.0, 0.0]])
        target = np.array([[0.0, 0.0]])
        testinput = np.array([0.0, 0.0])
        expected = np.array([0.0, 0.0])

        # Resultado dos calculos em sala de aula
        nweights = [np.array([[0.3, 0.8, 0.71],
                              [0.21, 0.5, 0.6]]),
                    np.array([[0.08, 0.38, 0.93],
                              [0.48, 0.28, 0.28]])]

        neural = spl.MLP(2, 1).fit(first, target)
        neural._weights[0] = weight1
        neural._weights[1] = weight2
        neural._forward(testinput)
        neural._backprop(expected)
        for old, new in zip(neural._weights, nweights):
            tst.assert_almost_equal(old, new, decimal=2)
