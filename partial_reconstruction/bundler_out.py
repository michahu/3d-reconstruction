import matplotlib.pyplot as plt

if __name__=='__main__':
    img1 = plt.imread('perm1-58.png')
    plt.figure(1)
    plt.subplot(131)
    plt.axis('off')
    plt.title('R2')
    plt.imshow(img1)

    plt.subplot(132)
    img2 = plt.imread('perm2-39.png')
    plt.title('R3')
    plt.axis('off')
    plt.imshow(img2)

    plt.subplot(133)
    img3 = plt.imread('perm3-66.png')
    plt.title('R4')
    plt.imshow(img3)
    plt.axis('off')

    plt.show()