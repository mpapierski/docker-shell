# select build image
FROM rust:1.37 as build

# create a new empty shell project
RUN USER=root cargo new --bin shell
WORKDIR /shell

# copy over your manifests
COPY ./Cargo.lock ./Cargo.lock
COPY ./Cargo.toml ./Cargo.toml

# this build step will cache your dependencies
RUN rustup target add x86_64-unknown-linux-musl
RUN cargo build --release --target x86_64-unknown-linux-musl
RUN rm src/*.rs

# copy your source tree
COPY ./src ./src

# build for release
# RUN rm ./target/release/deps/docker-shell*
RUN cargo build --release --target x86_64-unknown-linux-musl

# our final base
FROM scratch

# copy the build artifact from the build stage
COPY --from=build /shell/target/x86_64-unknown-linux-musl/release/docker-shell /bin/

# set the startup command to run your binary
ENTRYPOINT ["/bin/docker-shell"]
CMD ["/bin/docker-shell"]
