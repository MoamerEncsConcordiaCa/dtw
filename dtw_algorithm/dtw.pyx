
import sys

__author__ = 'mameri'


cdef check_ij_beam( int i, int j, int n1, int n2, float beam ):

        cdef float corr_j = (n2 * i) / float(n1)
        cdef float beam_n2 = (beam * n2)
        if j < (corr_j - beam_n2):
            return False
        if j > (corr_j + beam_n2):
            return False
        return True

cdef float euclidean_distance( list1, list2):
    cdef float s = 0.0
    cdef float sum_res = .0
    if len(list1) != len(list2):
        return float('Inf')

    for i in range(len(list1)):
        sum_res += (list1[i] - list2[i]) ** 2
    # sum_res = sum(map(lambda x, y: (x-y)**2, list1, list2)) ** 0.5
    s = sum_res ** 0.5
    return s


class DtwDisimillarity:

    def __init__(self):
        self.beam = 1.0
        self.feature1 = []
        self.feature2 = []
        self.n1 = 0
        self.n2 = 0

    # def __init__(self, feature1, feature2, beam):
    #     self.beam = beam
    #     self.feature1 = feature1
    #     self.feature2 = feature2
    #     self.n1 = len(self.feature1)
    #     self.n2 = len(self.feature2)

    def set_feature1(self, feature1):
        self.feature1 = feature1
        self.n1 = len(self.feature1)
        # print 'feature 1 len', self.n1

    def set_feature2(self, feature2):
        self.feature2 = feature2
        self.n2 = len(self.feature2)
        # print 'feature 2 len', self.n2

    def set_beam(self, beam):
        self.beam = 1.0
        if 0 < beam <= 1:
            self.beam = beam

    # @staticmethod
    # def euclidean_distance(list1, list2):
    #     if len(list1) != len(list2):
    #         return float('Inf')
    #     s = sum(map(lambda x, y: (x-y)**2, list1, list2)) ** 0.5
    #     return s



    def find_mapping(self, dp, ptr):
        # map finding
        map_dtw =[]
        i = self.n1 - 1
        j = self.n2 - 1
        while i > - 1 or j > -1 :
            map_dtw.append([i,j])
            if ptr[i][j] == 1:
                i -= 1
                j -= 1
            elif ptr[i][j] == 2:
                j -= 1
            elif ptr[i][j] == 3:
                i -= 1
            else:
                raise 'DTW path is not traceable exception'

        return map_dtw

    def dtw_dissimilarity(self):
        local_ratio = self.n1 / float(self.n2)
        if not 0.5 <= local_ratio <= 2:
            return float('Inf'), [], []

        dp = [ [-2  for j in range(0, self.n2) ] for i in range(0, self.n1) ]
        ptr = [ [-2 for j in range(0, self.n2) ] for i in range(0, self.n1) ]
        for i in range(0, self.n1):
            for j in range(0, self.n2):
                if self.beam == 1.0 or  check_ij_beam(i,j, self.n1, self.n2, self.beam):
                    dp[i][j] = -1
                    ptr[i][j] = -1

        for i in range(0, self.n1):
            for j in range(0, self.n2):
                if dp[i][j] != -1:
                    continue
                if i==0 and j==0:
                    dp[i][j] = euclidean_distance(self.feature1[i],
                                                       self.feature2[j])
                    ptr[i][j] = 1   # Diagonal
                elif i==0:
                    dp[i][j] = dp[i][j-1] + euclidean_distance(
                                    self.feature1[i], self.feature2[j])
                    ptr[i][j] = 2  # Left

                elif j==0:
                     dp[i][j] = dp[i - 1][j] + euclidean_distance(
                         self.feature1[i], self.feature2[j])
                     ptr[i][j] = 3  # top

                else:

                    dist = euclidean_distance(
                        self.feature1[i], self.feature2[j])

                    paths = []
                    if dp[i - 1][j - 1] >= 0:
                        paths.append([1, dist + dp[i - 1][j - 1] ] )

                    if dp[i][j - 1] >= 0:
                        paths.append([2, dist + dp[i][j - 1] ] )

                    if dp[i - 1][j] >= 0:
                        paths.append([3, dist + dp[i - 1][j] ] )

                    if len(paths) == 0:
                        return float('Inf'), [], 0.0

                    sorted_paths = sorted(paths, key=lambda x: x[1])
                    dp[i][j] = sorted_paths[0][1]
                    ptr[i][j] = sorted_paths[0][0]

        result = dp[self.n1 - 1][self.n2 - 1]

        try:
            dtw_map = self.find_mapping(dp, ptr)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return float('Inf'), [], 0.0

        dtw_len = len(dtw_map)
        return result, dtw_map, dtw_len

