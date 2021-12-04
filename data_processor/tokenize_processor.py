import numpy as np
import matplotlib.pyplot as plt

class TokenizeProcessor:
    def __init__(self, data_path):
        self.array = np.load(data_path).transpose((0, 3, 4, 1, 2))

    def tokenizing(self, window_size):
        output_shape = (self.array.shape[0], self.array.shape[1], self.array.shape[2], self.array.shape[3], (self.array.shape[4]-1) * pow(window_size, 2)+1)

        output_array = np.zeros(output_shape)
        padding = window_size // 2
        padded_array = np.pad(self.array, pad_width=((0,0),(padding,padding),(padding,padding),(0,0),(0,0)), mode='constant', constant_values=0)
        shape = padded_array.shape[1]
        for num_sample in range(self.array.shape[0]):
            for i in range(padding, shape-padding):
                for j in range(padding, shape-padding):
                    output_array[num_sample, i-padding, j-padding, :, :] = self.flatten_window(padded_array[num_sample, i-padding:i+padding+1, j-padding:j+padding+1, :, :], window_size)
        print(output_array.shape)
        return output_array

    def tokenizing_patch_segment(self, window_size):
        padding = window_size // 2
        padded_array = np.pad(self.array, pad_width=((0, 0), (padding, padding), (padding, padding), (0, 0), (0, 0)),
                              mode='constant', constant_values=0)
        shape = padded_array.shape[1]

        # output_shape = (self.array.shape[0], self.array.shape[1], self.array.shape[2], self.array.shape[3], (self.array.shape[4]-1) * pow(window_size, 2)+1)
        output_array = []
        label_array = []
        recon_array = np.zeros((226,226))
        for num_sample in range(self.array.shape[0]):
            for i in range(padding, shape-padding, 1+padding):
                for j in range(padding, shape-padding, 1+padding):
                    output, label = self.flatten_window(padded_array[num_sample, i-padding:i+padding+1, j-padding:j+padding+1, :, :], window_size)

                    iidx = int((i-padding)/(padding*2))
                    jidx = int((j-padding)/(padding*2))
                    label_array.append(label)
                    output_array.append(output)
                    # recon_array[i - window_size // 2:i + window_size // 2 + 1,
                    # j - window_size // 2:j + window_size // 2 + 1] = label_array[iidx*112 + jidx][5, :].reshape(
                    #     (window_size, window_size), order='F')

            # plt.imshow(recon_array)
            # plt.show()
        output_array = np.stack(output_array, axis=0)
        label_array = np.stack(label_array, axis=0)
        print(output_array.shape)
        return output_array, label_array

    def flatten_window(self, array, window_size):
        output_array = np.zeros((array.shape[2], (array.shape[3]-1)*pow(window_size,2)))
        label = np.zeros((array.shape[2], pow(window_size, 2)))
        for time in range(array.shape[2]):
            output_array[time, :output_array.shape[1]] = array[:, :, time, :5].flatten('F')
            label[time, :] = array[window_size//2, window_size//2, time, 5].flatten('F')
        return output_array, label


if __name__=='__main__':
    window_size = 3
    tokenize_processor = TokenizeProcessor('/Users/zhaoyu/PycharmProjects/CalFireMonitoring/data_train_proj3/proj3_train_img_v2.npy')
    tokenized_array, label_array = tokenize_processor.tokenizing_patch_segment(window_size)
    np.nan_to_num(tokenized_array)
    # np.save('../data/proj3_test_w'+str(window_size)+'.npy', tokenized_array.reshape(-1,10,pow(window_size,2)*5+1))
    np.save('../data/proj3_test_w' + str(window_size) + 'patch_seg.npy',
            tokenized_array)
    np.save('../data/proj3_test_w' + str(window_size) + 'label.npy',
            label_array)
    # for i in range(tokenized_array.shape[0]):
    #     for j in range(tokenized_array.shape[3]):
    #         plt.subplot(211)
    #         ch_label = pow(window_size,2)*5
    #         ch_i4 = pow(window_size,2)*3+pow(window_size,2)//2
    #         plt.imshow(
    #             (tokenized_array[i, :, :, j, ch_label] - tokenized_array[i, :, :, j, ch_label].min()) - (
    #                         tokenized_array[i, :, :, j, ch_label].max() - tokenized_array[i, :, :, j, ch_label].min()))
    #         plt.subplot(212)
    #         plt.imshow(
    #             (label_array[i, :, :, j, ch_i4] - tokenized_array[i, :, :, j, ch_i4].min()) - (
    #                         tokenized_array[i, :, :, j, ch_i4].max() - tokenized_array[i, :, :, j, ch_i4].min()))
    #         plt.savefig('../plt/' + str(i) + str(j) + '.png')
    #         plt.show()
    # def standardize(array):
    #     return (array-array.min())/(array.max()-array.min())
    #
    #
    # img = np.zeros((226, 226))
    # label = np.zeros((226, 226))
    # for num in range(58):
    #     for k in range(10):
    #         for i in range(1, 224, 2):
    #             for j in range(1, 224, 2):
    #                 iidx = int((i - 1) / (1 * 2))
    #                 jidx = int((j - 1) / (1 * 2))
    #                 label[i - window_size // 2:i + window_size // 2 + 1,
    #                 j - window_size // 2:j + window_size // 2 + 1] = label_array[iidx*112 + jidx][k, :].reshape(
    #                     (window_size, window_size), order='F')
    #                 img[i - window_size // 2:i + window_size // 2 + 1,
    #                 j - window_size // 2:j + window_size // 2 + 1] = tokenized_array[iidx * 112 + jidx][k, 27:36].reshape(
    #                     (window_size, window_size), order='F')
    #
    #         plt.subplot(211)
    #         plt.imshow(standardize(img))
    #         plt.subplot(212)
    #         plt.imshow(standardize(label))
    #         plt.savefig('../plt_test/' + str(num) + str(k) + '.png')
    #         plt.show()

