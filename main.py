from app.tomograph import Tomograph
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, ArtistAnimation


def update_frame(frame, tomograph, axarr):
    print(frame)
    tomograph.measure(with_mask=True)
    tomograph.construct()
    tomograph.next_step()

    axarr[1].clear()
    axarr[1].imshow(tomograph.sinogram, cmap="gray", aspect="auto")
    axarr[2].clear()
    axarr[2].imshow(tomograph.constructed_img, cmap="gray", aspect="auto")

    return axarr,


def main():
    alpha = 0.5
    tomograph = Tomograph(alpha, 130, 1, "./data/test_details_240.png")
    f, axarr = plt.subplots(1, 3, figsize=(12, 3))

    axarr[0].set_title('Original img')
    axarr[0].imshow(tomograph.orginal_img, cmap="gray", aspect="auto")
    axarr[1].set_title('Current row of sinogram')
    axarr[2].set_title('Reconstructed img')

    # ims = []
    # for i in range(int(180 / alpha)):
    #     print(i, '/', int(180 / alpha)-1)
    #     tomograph.measure(with_mask=True)
    #     tomograph.construct()
    #     tomograph.next_step()
    #     ims.append((
    #         axarr[1].imshow(tomograph.sinogram, cmap="gray", aspect="auto"),
    #         axarr[2].imshow(tomograph.constructed_img, cmap="gray", aspect="auto")
    #     ))
    # print(tomograph.get_error())

    anim = FuncAnimation(f, update_frame, init_func=lambda: 0, frames=int(180 / alpha), fargs=(tomograph, axarr), interval=1, repeat=False)
    # anim = ArtistAnimation(f, ims, interval=50, blit=True)

    # plt.show()


if __name__ == "__main__":
    main()
