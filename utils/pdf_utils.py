from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .embeddings_utils import load_embeddings, save_embeddings, generate_embeddings, load_faiss_index, create_vector_index, save_faiss_index
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import getpass

samp_chunks = ["""ECEN 637 Numerical Methods in
Electromagnetics
Credits 3. 3 Lecture Hours. Numerical methods of engineering
electromagnetics, including finite differencing, finite difference time
domain, finite elements, the method of moments and parabolic equation.
Prerequisite: ECEN 322.""",
"""ECEN 638 Antennas and Propagation
Credits 3. 3 Lecture Hours. Application of Maxwell's equations to
determine electromagnetic fields of antennas; radiation, directional
arrays, impedance characteristics, aperture antennas. Prerequisite:
ECEN 322.""",
"""ECEN 639 Microwave Circuits
Credits 3. 3 Lecture Hours. Introduction to high frequency systems
and circuits; provides background information needed to understand
fundamentals of microwave integrated circuits; includes usage of
S-parameters, Smith Charts, stability considerations in designing
microwave circuits; utilizes CAD program "Super Compact"
demonstrating design synthesis optimization and analysis of monolithic
devices and circuits. Prerequisite: Graduate classification.""",
"""ECEN 640 Thin Film Science and
Technology
Credits 3. 3 Lecture Hours. 1 Lab Hour. Thin film technology in
semiconductor industry; topics include the basic growth mechanisms for
thin films (growth models, lattice matching epitaxy and domain matching
epitaxy), the instrumental aspects of different growth techniques and
advanced topics related to various applications. Prerequisites: Graduate
classification.""",
"""ECEN 641 Microwave Solid-State
Integrated Circuits
Credits 3. 3 Lecture Hours. Microwave two-terminal and three-terminal
solid-state devices; waveguide and microstrip solid-state circuits; theory
and design of microwave mixers, detectors, modulators, switches, phase
shifters, oscillators and amplifiers. Prerequisite: ECEN 322.""",
"""ECEN 642 Digital Image Processing and
Computer Vision
Credits 3. 3 Lecture Hours. Digital Image Processing and computer vision
techniques; stresses filtering, intensity transformations, compression,
restoration and reconstruction, morphology, segmentation, feature
extraction and pattern classification. Prerequisite: ECEN 447 and
ECEN 601, or approval of instructor.""",
"""ECEN 643 Electric Power System
Reliability
Credits 3. 3 Lecture Hours. Design and application of mathematical
models for estimating various measures of reliability in electric power
systems. Prerequisite: ECEN 460 or approval of instructor.""",
"""ECEN 644 Discrete-Time Systems
Credits 3. 3 Lecture Hours. Linear discrete time systems analysis using
time domain and transform approaches; digital filter design techniques
with digital computer implementations. Prerequisite: ECEN 601, or
approval of instructor."""]

def read_pdf(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def split_text(text, chunk_size=700, chunk_overlap=400):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(text=text)
    return chunks

def save_chunks_to_file(chunks, file_path):
    with open(file_path, 'w') as file:
        for chunk in chunks:
            file.write(chunk + '\n---\n')

def pdf_to_vector_index(pdf, store_name, embeddings_model):
    text = read_pdf(pdf)
    chunks = split_text(text)
    save_chunks_to_file(chunks, 'saved_chunks.txt')
    #chunks = samp_chunks
    print("Len chunks:", len(chunks))
  
    if os.path.exists(
        os.path.join('embeddings_store', store_name + '.pkl')
        ) and os.path.exists(
            os.path.join('embeddings_store', store_name + '.faiss')
        ):
        print("In here")
        # embeddings = load_embeddings(store_name)
        vector_index = load_faiss_index(store_name, embeddings_model)
        print("$$$ Loaded saved embeddings")
        return vector_index
    else:
        print("$$$$ Generating embeddings")
        embedded_chunks = generate_embeddings(chunks, embeddings_model)
        vector_index = create_vector_index(chunks, embedded_chunks, embeddings_model)
        # save_embeddings(embeddings, store_name)
        save_faiss_index(vector_index, store_name)
        print("$$$ Generated embeddings")
    return vector_index
