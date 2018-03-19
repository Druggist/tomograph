from app.tomograph import Tomograph
import matplotlib.pyplot as plt


def main():
    aplha = 0.5

    tomograph = Tomograph(aplha, 100, 1, "./data/test_balls.png")
    for i in range(int(360 / aplha)):
        tomograph.measure()
        tomograph.next_step()
        tomograph.construct(i)
    # tomograph.normalize()
    detectors = tomograph._get_detectors()

    f, axarr = plt.subplots(1, 3, figsize=(16,8))
    axarr[0].set_title('Original img')
    axarr[0].imshow(tomograph.orginal_img, cmap="gray")
    # for d in detectors:
    #     axarr[0].plot((d.a, d.x), (d.b, d.y))

    axarr[1].set_title('Current row of sinogram')
    axarr[1].imshow(tomograph.sinogram, cmap="gray")

    axarr[2].set_title('Reconstructed img')
    axarr[2].imshow(tomograph.constructed_img, cmap="gray")

    plt.show()


if __name__ == "__main__":
    main()
