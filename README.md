Fountain Codes
=========

#### One to many data transmission across a flaky network

Fountain codes provide a way for data to be transmitted across a lossy network connection from a single source to many users. The name "fountain code" arises because fountain codes behave analogously to a fountain. A file being transmitted is analogous to a glass of water from the fountain. To fill the glass (or reconstruct the file), you need to catch enough droplets from the fountain such that your glass becomes full. It isn't important which droplets of water you catch in your glass; once you have enough, the glass is full (and the file can be reconstructed). Fountain codes work in the same way, but with information instead of water. The data being transferred can be algorithmically encoded as an arbitrarily large number of chunks, or droplets, that can be sent over the network. The receiving client then needs to receive some number of these droplets in order to reconstruct the original file. It doesn't matter which droplets are received or in what order they are received, and it doesn't matter which are lost during transmission. This is the beauty of fountain codes. As long as a sufficient number of droplets are received, the original file can be reconstructed completely.

We'll explore the motivation behind fountain codes, how these codes are implemented, and why their properties can be useful for file transfer over the internet.

One application that at a glance seems to merit use of fountain codes is torrent sites. For users looking to download large files over a possibly temperamental connection, the fountain code seems ideal. Even if the connection is lost for a substantial period of time, which may be unavoidable with peer-to-peer connections, the fountain code will continue to work without the need for sending confirmation bits indicating that packets have been received. The result is that a file distributor can start a connection with any user, and they can start spewing out droplets for a particular file; they are the fountain. If the client stops catching the droplets, someone else with the file can apply the same algorithm to continue broadcasting the file without knowing how much of the file has been received or which parts of the previous transmission were dropped. While this seems ideal for peer to peer file transfer, it has one fatal flaw that fountain codes cannot resolve.

The flaw I speak of is a security vulnerability. With applications like BitTorrent, a sha1 hash of the file being transferred is used to verify that the sender of the file can be trusted to send the file, instead of sending malicious software to run on your computer or a corrupted version of the file. We are able to verify that the data being transmitted can be trusted using by comparing the hash of the file to the hash we received from a trusted source. When using fountain codes, the droplets that are sent over the network cannot be verified, because they are generated dynamically during transmission, and there is an arbitrarily large number of these chunks. It is therefore infeasible to precompute the hash of all possible droplets at the start of the transmission. One solution for this is to send the hash of the entire file, but that cannot be checked until the transmission has completed, which is too late in the process to be practical. Ideally we would be able to detect corrupt files during the transmission, like we can do when the file is transmitted sequentially, but unfortunately straightforward application of fountain codes does not allow this.

The most remarkable aspect of fountain codes is that any droplets can be caught and the file can still be reconstructed. To see how this is possible, we look now at one implementation of fountain codes.

The encoding scheme for this implementation is simple. First, the file is broken into chunks that will be used to create the droplets for the fountain. We use 32 character chunks by default for this implementation, but any size could be used. Larger chunks are more likely to be dropped on the lossy connection we're using, but decrease the number of droplets that have to be received, and so the chunk size is a tradeoff that must be carefully balanced. For each droplet that will be transmitted, we will select some number of these chunks, and XOR them together. The number of chunks to combine in this manner also affects the performance of the algorithm; in our implementation we choose a small number (single digit small) at random for the number of chunks for a particular droplet. Suppose for our first droplet we choose chunks 1, 3, and 7. These chunks are XOR'd together and the result is transmitted over the network along with enough information for the receiving client to figure out which chunks were included.

There are two ways to supply this information. The first, and simplest, is to include the chunk numbers in the transmitted droplet. With larger numbers of chunks, this amount of information could be prohibitively large, and since the number of chunks in a droplet varies, this method would complicate the droplet protocol because it would no longer be a fixed width protocol. The second method of transmitting the chunk numbers is for the sender and receiver to agree on a random number generator that will be used to generate the chunk numbers. The sender then merely includes the seed used to create the chunk numbers inside the droplet. When the droplet is caught, the receiving client then uses the same random number generator with the same seed to determine which chunks were included in the droplet.

As droplets are caught, a client can begin decoding the data and recovering the original chunks. Here is the method for doing so. As droplets are caught, the receiving client stores them all. They need sufficient information to determine the contents of each chunk of the original file uniquely. Suppose the receiving client has droplets with chunk numbers (1, 3, 7), (1, 3, 4), and (1, 4, 7). Then the XOR of these three chunks will produce precisely chunk 1 of the original file. The algorithm works by having the client simply wait until it has sufficient information to reconstruct all of the chunks. These are then concatenated together to produce the original file. However, implementing this method of reconstruction naively is prohibitively slow due to the number of possible combinations of droplets. Instead, the algorithm waits for droplets that contain single chunks. These are used to determine the contents of sum chunks, and are used to puzzle apart the contents of other droplets. If we have three droplets with chunk numbers (1), (1, 2), and (1, 2, 3) then chunks 1, 2, and 3 can all be determined in this manner.

I implemented the encoding and decoding algorithms here. I have set up a server as a fountain at [http://fountain.herokuapp.com](http://fountain.herokuapp.com). You can watch as the web client receives chunks from the fountain and is slowly able to reconstruct the original data, which I chose to be this essay. I include the source code in the attached appendix, and it is also available on GitHub at [https://github.com/dbieber/fountaincode](https://github.com/dbieber/fountaincode).

With this algorithm implemented, I was able to examine its efficiency some. Experimentally I've found that the client typically has to receive about 4 times the amount of data being transferred before being able to reconstruct the entire file. This implementation is not the industry standard, but it is the easiest implementation of fountain codes to implement and to explain. By changing the method of random number selection, fountain codes can be improved. These improvements still rely on the model of catching droplets, but are more suitable to real world applications.

However, fountain codes have the downside of transmitting files only in their entirety. If insufficient droplets are received, there is no guarantee that any continuous part of the file will be readable. Other methods exist for applications where it would be better to receive the file in continuous segments. For such applications, such as watching YouTube videos, streaming data is more applicable. The water analogues never seem to end.

#### Relevant Links

My source: [https://github.com/dbieber/fountaincode](https://github.com/dbieber/fountaincode)

My web application, a demo of fountain codes: [http://fountain.herokuapp.com/](http://fountain.herokuapp.com/)

Wikipedia's explanation of fountain codes: [http://en.wikipedia.org/wiki/Fountain\_code](http://en.wikipedia.org/wiki/Fountain\_code)

A particularly good explanation of fountain codes: [http://blog.notdot.net/tag/fountain-codes](http://blog.notdot.net/tag/fountain-codes)

#### Source Files
[fountain.py](fountain.py) defines the Fountain, produces Droplets according to the Fountain Code implementation discussed in the paper.

[droplet.py](droplet.py) defines the Droplet, containing a seed and the XOR'd data.

[glass.py](glass.py) defines a Glass, used to collect Droplets and reconstruct the original data

[utils.py](utils.py) contains helper functions used to make the Fountain and Droplets compatible.

[client.py](client.py) generates a fountain for a particular message, this essay.

[app.py](app.py), [Procfile](Procfile), [requirements.txt](requirements.txt) turn this project into a web app, runnable on Heroku.

[glass.html](templates/glass.html), [home.html](templates/home.html) are templates, used by the web app to render pages.
