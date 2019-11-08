FROM golang:alpine AS builder
ADD sentence.go .

RUN apk update && apk add --no-cache git
RUN go get -d -v

# The parameters are important for scratch images to work
RUN CGO_ENABLED=0 GOOS=linux go build -o /go/bin/sentence

RUN adduser -S scratchuser
RUN chown scratchuser /go/bin/sentence

FROM scratch
COPY --from=builder /go/bin/sentence /sentence
COPY --from=builder /etc/passwd /etc/passwd
USER scratchuser
CMD ["/sentence"]
