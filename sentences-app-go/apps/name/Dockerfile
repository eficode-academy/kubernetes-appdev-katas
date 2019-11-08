FROM golang:alpine AS builder
ADD name.go .

RUN apk update && apk add --no-cache git
RUN go get -d -v

# The parameters are important for scratch images to work
RUN CGO_ENABLED=0 GOOS=linux go build -o /go/bin/name

RUN adduser -S scratchuser
RUN chown scratchuser /go/bin/name

FROM scratch
COPY --from=builder /go/bin/name /name
COPY --from=builder /etc/passwd /etc/passwd
USER scratchuser
CMD ["/name"]
