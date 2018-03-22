from app.tomograph import Tomograph
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def update_frame(frame, tomograph, axarr):
    print(frame)
    tomograph.measure()
    tomograph.construct()
    tomograph.next_step()

    axarr[1].clear()
    axarr[1].imshow(tomograph.sinogram, cmap="gray", aspect="auto")
    axarr[1].set_xlabel('alpha')
    axarr[1].set_ylabel('detector')
    axarr[2].clear()
    axarr[2].imshow(tomograph.constructed_img, cmap="gray", aspect="auto")

    return axarr,


def main():
    alpha = 1
    tomograph = Tomograph(alpha, 150, 0.5, "./data/test_alien.png")

    for i in range(int(180 / alpha)):
        print(i, '/', int(180 / alpha)-1)
        tomograph.measure(with_mask=True)
        tomograph.construct()
        tomograph.next_step()

    f, axarr = plt.subplots(1, 3, figsize=(12, 3))
    axarr[0].set_title('Original img')
    axarr[0].imshow(tomograph.orginal_img, cmap="gray", aspect="auto")

    axarr[1].set_title('Current row of sinogram')
    axarr[1].imshow(tomograph.sinogram, cmap="gray", aspect="auto")

    axarr[2].set_title('Reconstructed img')
    axarr[2].imshow(tomograph.get_constructed_img(), cmap="gray", aspect="auto")

    # anim = FuncAnimation(f, update_frame, init_func=lambda: 0, frames=int(180 / alpha), fargs=(tomograph, axarr),
    #                      interval=1, repeat=False)
    plt.show()


if __name__ == "__main__":
    main()
