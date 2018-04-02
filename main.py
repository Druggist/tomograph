from app.tomograph import Tomograph
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse

parser = argparse.ArgumentParser(description='Process image like tomograph.')
parser.add_argument('--anim', default=False, type=bool, help='whether to animate output')
parser.add_argument('--input', default="./data/test_details_240.png", help='input image path')
parser.add_argument('--alpha', default=5, type=float, help='alpha step')
parser.add_argument('--count', default=100, type=int, help='count of detectors')
parser.add_argument('--span', default=1, type=float, help='span between detectors')

def update_frame(frame, f, tomograph, axarr):
    print(frame)
    tomograph.measure(with_mask=True)
    tomograph.construct()
    tomograph.next_step()

    axarr[1].clear()
    axarr[1].set_title('Sinogram')
    axarr[1].imshow(tomograph.sinogram, cmap="gray", aspect="auto")
    axarr[2].clear()
    axarr[2].set_title('Reconstructed image')
    axarr[2].imshow(tomograph.constructed_img, cmap="gray", aspect="auto")
    f.text(0.91, 0.5, 'err: ' + str(tomograph.get_error()), bbox={'facecolor':'red', 'pad': 5})
    return axarr,


def main(args):
    print(args)
    tomograph = Tomograph(args.alpha, args.count, args.span, args.input)
    f, axarr = plt.subplots(1, 3, figsize=(12, 3))
    axarr[0].set_title('Original image')
    axarr[0].imshow(tomograph.orginal_img, cmap="gray", aspect="auto")

    if not args.anim:
        for i in range(int(180 / args.alpha)):
            print(i, '/', int(180 / args.alpha)-1)
            tomograph.measure(with_mask=True)
            tomograph.construct()
            tomograph.next_step()

        axarr[1].set_title('Sinogram')
        axarr[1].imshow(tomograph.sinogram, cmap="gray", aspect="auto")
        axarr[2].set_title('Reconstructed image')
        axarr[2].imshow(tomograph.constructed_img, cmap="gray", aspect="auto")
        f.text(0.91, 0.5, 'err: ' + str(tomograph.get_error()), bbox={'facecolor':'red', 'pad': 5})
    else:
        anim = FuncAnimation(f, update_frame, init_func=lambda: 0, frames=int(180 / args.alpha), fargs=(f, tomograph, axarr), interval=1, repeat=False)
    plt.show()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
