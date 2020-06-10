import matplotlib.pyplot as plt
import matplotlib.patches as patches
import torch
import numpy as np
from PIL import Image 

H, W = 300, 300

def plot_data_sample(dataset, idx):
    
    sample = dataset.__getitem__(idx)
    x,y, h, w = sample['bbox'].data
    fig, ax = plt.subplots(1)
    ax.imshow(sample['image'])
    box = patches.Rectangle((x,y),h,w, edgecolor='r', facecolor="none")
    ax.add_patch(box)
    plt.title(sample['bbox'])
    plt.show()
    
def plot_transformed_data_sample(dataset, idx, transform):

    sample = dataset.__getitem__(idx)
    transformed_image = sample['image']\
                        .permute(1,2,0)\
                        .clamp(0,1)

    x,y, h, w = sample['bbox'].data
    
    fig, ax = plt.subplots(1)
    ax.imshow(transformed_image)
    box = patches.Rectangle((x,y),
                            h, w, 
                            edgecolor='r', facecolor="none")
    ax.add_patch(box)
    plt.title("Transformed sample image")
    plt.show()
    
    
def visualize_model(model, dataloaders, class_names, num_images=10):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    was_training = model.training
    model.to(device)
    model.eval()
    images_so_far = 0
    fig = plt.figure()

    with torch.no_grad():
        for i, batch in enumerate(dataloaders['val']):
            inputs = batch['image'].to(device, dtype=torch.float)
            labels = batch['label'].to(device, dtype=torch.int64)

            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            
            fig, axs = plt.subplots(2,5)
            for j in range(inputs.size()[0]):
                images_so_far += 1
                axs[j//5, j%5].axis('off')
                axs[j//5, j%5].set_title('predicted: {}'.format(class_names[preds[j]]))
                imshow(inputs.cpu().data[j], axs[j//5, j%5])

                if images_so_far == num_images:
                    model.train(mode=was_training)
                    return
        model.train(mode=was_training)