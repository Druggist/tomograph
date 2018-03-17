from app.tomograph import Tomograph
import matplotlib.pyplot as plt


def main():
    tomograph = Tomograph(10, 50, 2, "./data/test_balls.png")
    for i in range(36):
        tomograph.measure()
        tomograph.next_step()
    detectors = tomograph._get_detectors()

    f, axarr = plt.subplots(1, 3, figsize=(16,8))
    axarr[0].set_title('Original img')
    axarr[0].imshow(tomograph.orginal_img, cmap="gray")
    # for d in detectors:
    #     axarr[0].plot((d.a, d.x), (d.b, d.y))

    axarr[1].set_title('Current row of sinogram')
    axarr[1].imshow(tomograph.sinogram, cmap="gray")

    axarr[2].set_title('Reconstructed img')
    # axarr[2].imshow()

    plt.show()


if __name__ == "__main__":
    main()
