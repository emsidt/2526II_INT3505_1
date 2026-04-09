import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;

@service({
  title: "Library Management API"
})
namespace LibraryApi;

model Book {
  id: int32;
  title: string;
  author: string;
  published_year: int32;
}

model BookInput {
  title: string;
  author: string;
  published_year?: int32;
}

@route("/books")
interface Books {
  @get list(): Book[];

  @post create(@body body: BookInput): Book;

  @get @route("/{bookId}")
  getById(@path bookId: int32): Book;

  @put @route("/{bookId}")
  update(@path bookId: int32, @body body: BookInput): Book;

  @delete @route("/{bookId}")
  delete(@path bookId: int32): string;
}