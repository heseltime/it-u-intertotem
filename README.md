# it-u-intertotem

This is the software repo for a system running a non-standard seismograph, welcome!

**Run**: the setup depends on a virtual env called it-u, so to run, in the base it-u-intertotem directory, simply ...

```
source it-u/bin/activate
python main.py
```

**Project Structure**:

```
it-u-intertotem/
│
├── code_templates/ # sample scripts
├── it-u/ # venv scripts
├── main.py # main earthquake logic, calls communication script at the end
├── communication/
│   ├── __init__.py  # (empty file to make this directory a package)
│   └── communication.py  # communication script
└── output/  # directory where WAV files are stored
```

## 🌍 From the [Project Proposal](https://github.com/heseltime/it-u-intertotem/blob/main/project-proposal.pdf)

This project aims to engage how we experience seismic data by creating an experience (artistic) and non-standard seismograph that merges cultural artefact and elements of nature.

In many cultures, totems symbolize a deep connection between the natural world, spiritual beliefs, and community identity. Drawing on this notion, our project seeks to create a bridge between the science of seismology and the cultural and psychological, physiological experiences.

![image](https://github.com/user-attachments/assets/d5fbde86-16aa-4a73-8cec-b953ca6096df)


## 🛠️ Hardware 

The system should run on **raspberry pi** in either a monolithic or a distributed mode, interfacing with **multiple speakers** (mono) or one speaker at a time (distributed). The other hardware are **3D-printed pi and/or speaker casings** implementing the totemic theme, see below (section "Totems").

But first, establishing the communicative mode is the end-goal of project stage 1, as in ...

## 📅 Project Stages

- 1: Get components communicating
- 2: Fleshing it out (Prototype)
- 3: Wrap, Concept for Larger Scale Product

## 🪆 Totems

Totems are central to the project, representing the fusion of technology, art, and cultural symbolism. The totems are designed as 3D-printed casings for the Raspberry Pi and speakers, embodying natural and spiritual elements. These casings can take various forms, reflecting the cultural themes and aesthetic principles tied to the seismograph's outputs.

Each totem is intended to resonate with its environment, whether through its design, sound, or placement. The visual and auditory aspects of the totems are meant to create a holistic sensory experience that connects the viewer to the data in a meaningful way.

The totems not only serve as functional hardware components but also as artistic expressions, allowing the project to transcend traditional scientific boundaries and engage audiences on a more personal and emotional level.
