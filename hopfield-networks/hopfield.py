'''
Description: CS5340 - Hopfield Network
Name: Your Name, Your partner's name
Matric No.: Your matric number, Your partner's matric number
'''


import matplotlib
matplotlib.use('Agg')
import numpy as np
import glob
import matplotlib.pyplot as plt
from PIL import Image, ImageOps



def load_image(fname):
    img = Image.open(fname).resize((32, 32))
    img_gray = img.convert('L')
    img_eq = ImageOps.autocontrast(img_gray)
    img_eq = np.array(img_eq.getdata()).reshape((img_eq.size[1], -1))
    return img_eq


def binarize_image(img_eq):
    img_bin = np.copy(img_eq)
    img_bin[img_bin < 128] = -1
    img_bin[img_bin >= 128] = 1
    return img_bin


def add_corruption(img):
    img = img.reshape((32, 32))
    t = np.random.choice(3)
    if t == 0:
        i = np.random.randint(32)
        img[i:(i + 8)] = -1
    elif t == 1:
        i = np.random.randint(32)
        img[:, i:(i + 8)] = -1
    else:
        mask = np.sum([np.diag(-np.ones(32 - np.abs(i)), i)
                       for i in np.arange(-4, 5)], 0).astype(np.int)
        img[mask == -1] = -1
    return img.ravel()


def learn_hebbian(imgs):
    img_size = np.prod(imgs[0].shape)
    ######################################################################
    ######################################################################
    weights = np.zeros((img_size, img_size))
    bias = np.zeros(img_size)
    # Complete this function
    # You are allowed to modify anything between these lines
    # Helper functions are allowed
    #######################################################################
    #######################################################################
    for img in imgs:
        img_array = np.asarray(img).reshape(-1)
        # for i in range(img_size):
        #     for j in range(img_size):
        #         #TODO: Can optimise by finding weights above diagonal only
        #         if i != j:
        #             weights[i][j] += (img_array[i]) * (img_array[j])
        weights += np.dot(img_array.reshape((img_size,1)), img_array.reshape((1,img_size)))

        np.fill_diagonal(weights,0)

    return weights, bias


def learn_maxpl(imgs):
    img_size = np.prod(imgs[0].shape)
    ######################################################################
    ######################################################################
    weights = np.zeros((img_size, img_size))
    bias = np.zeros(img_size)
    # Complete this function
    # You are allowed to modify anything between these lines
    # Helper functions are allowed
    #######################################################################
    #######################################################################
    return weights, bias


def plot_results(imgs, cimgs, rimgs, fname='result.png'):
    '''
    This helper function can be used to visualize results.
    '''
    img_dim = 32
    assert imgs.shape[0] == cimgs.shape[0] == rimgs.shape[0]
    n_imgs = imgs.shape[0]
    fig, axn = plt.subplots(n_imgs, 3, figsize=[8, 8])
    for j in range(n_imgs):
        axn[j][0].axis('off')
        axn[j][0].imshow(imgs[j].reshape(img_dim, img_dim), cmap='Greys_r')
    axn[0, 0].set_title('True')
    for j in range(n_imgs):
        axn[j][1].axis('off')
        axn[j][1].imshow(cimgs[j].reshape(img_dim, img_dim), cmap='Greys_r')
    axn[0, 1].set_title('Corrupted')
    for j in range(n_imgs):
        axn[j][2].axis('off')
        axn[j][2].imshow(rimgs[j].reshape((img_dim, img_dim)), cmap='Greys_r')
    axn[0, 2].set_title('Recovered')
    fig.tight_layout()
    plt.savefig(fname)

def flatten_img(img):
    return np.asarray(img).reshape(-1)

def unflatten_img(flat_img):
    return np.reshape(flat_img, (32, 32))

def show_img(img):
    w, h = 32, 32
    data = np.zeros((h, w, 3), dtype=np.uint8)
    #data[256, 256] = [255, 0, 0]
    for i in range(32):
        for j in range(32):
            if img[i][j] == -1:
                data[i][j] = [0, 0, 0]
            else:
                data[i][j] = [255,255,255]

    img = Image.fromarray(data, 'RGB')
    img.save('my.png')
    img.show()

def recover_img(cimg, W, b):
    img_size = np.prod(cimg.shape)
    img = np.copy(cimg)

    order = []
    for i in range(img_size):
        order.append(i)

    iterations = 0
    while True:
        # in every iteration, initialise noChange to True
        noChange = True
        iterations += 1
        np.random.shuffle(order)
        for index in order:
            sum = 0
            for i in range(img_size):
                if i != index:
                    sum += W[i][index] * img[i] + b[i]
            if sum >= 0:
                if img[index] != 1:
                    noChange = False
                    img[index] = 1
            else:
                if img[index] != -1:
                    noChange = False
                    img[index] = -1

        # Check if nothing changed
        if noChange == True:
            break

    rimg = img
    print('Iterations Taken:', iterations)
    return rimg

def recover(cimgs, W, b):
    img_size = np.prod(cimgs[0].shape)
    ######################################################################
    ######################################################################
    rimgs = []
    # Complete this function
    # You are allowed to modify anything between these lines
    # Helper functions are allowed
    #######################################################################
    #######################################################################

    for cimg in cimgs:
        rimg = recover_img(cimg, W, b)
        rimgs.append(unflatten_img(rimg))

    return rimgs


def main():
    # Load Images and Binarize
    ifiles = sorted(glob.glob('images/*'))
    timgs = [load_image(ifile) for ifile in ifiles]
    imgs = np.asarray([binarize_image(img) for img in timgs])
    for img in (imgs):
        plt.figure(0)
        plt.imshow(img)


    # Add corruption
    cimgs = []
    for i, img in enumerate(imgs):
        cimgs.append(add_corruption(np.copy(imgs[i])))
    cimgs = np.asarray(cimgs)

    # Recover 1 -- Hebbian
    Wh, bh = learn_hebbian(imgs)
    rimgs_h = recover(cimgs, Wh, bh)
    np.save('hebbian.npy', rimgs_h)

    # Recover 2 -- Max Pseudo Likelihood
    Wmpl, bmpl = learn_maxpl(imgs)
    rimgs_mpl = recover(cimgs, Wmpl, bmpl)
    np.save('mpl.npy', rimgs_mpl)

    # TODO: Remove before submission
    print("Length", len(rimgs_h))
    cimg = unflatten_img(cimgs[0])
    rimg = rimgs_h[0]
    # for cimg in cimgs:
    #     show_img(unflatten_img(cimg))
    show_img(cimg)
    show_img(rimg)

if __name__ == '__main__':
    main()
