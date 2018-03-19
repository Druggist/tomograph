from app.tomograph import Tomograph
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation, FuncAnimation


def update_frame(frame, tomograph, axarr):
    print(frame)
    tomograph.measure()
    tomograph.construct()
    tomograph.next_step()

    axarr[1].clear()
    axarr[1].imshow(tomograph.sinogram, cmap="gray")
    axarr[2].clear()
    axarr[2].imshow(tomograph.constructed_img, cmap="gray")

    return axarr


def main():
    alpha = 0.1
    tomograph = Tomograph(alpha, 2000, 0.1, "./data/test_details.png")

    f, axarr = plt.subplots(1, 3, figsize=(16, 8))
    axarr[0].set_title('Original img')
    axarr[0].imshow(tomograph.orginal_img, cmap="gray")

    # for d in detectors:
    #     axarr[0].plot((d.a, d.x), (d.b, d.y))

    ims = []
    axarr[1].set_title('Current row of sinogram')
    ims.append(axarr[1].imshow(tomograph.sinogram, cmap="gray"))

    axarr[2].set_title('Reconstructed img')
    ims.append(axarr[2].imshow(tomograph.constructed_img, cmap="gray"))

    anim = FuncAnimation(f, update_frame, init_func=lambda: 0, frames=int(360/alpha), fargs=(tomograph, axarr), interval=1, repeat=False)

    plt.show()


if __name__ == "__main__":
    main()
