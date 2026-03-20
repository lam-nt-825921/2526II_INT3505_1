import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;

// --- Siêu Dữ Liệu Chung ---
@service(#{
  title: "Khảo sát API Quản lý Thư viện (TypeSpec)"
})
@server("http://localhost:8000", "Máy chủ cục bộ")
namespace LibraryService;

// --- Định nghĩa Cấu Trúc Types ---
enum BookStatus {
  available: "available",
  borrowed: "borrowed"
}

model Book {
  @key("id")
  @doc("Khóa chính của sách")
  id: int32;

  title: string;
  author: string;
  status: BookStatus;
}

model BookInput {
  title: string;
  author: string;
  status: BookStatus;
}

model User {
  @key("id")
  id: int32;
  name: string;
  email: string;
}

model UserInput {
  name: string;
  email: string;
}

model ErrorResponse {
  detail: string;
}

// --- Định nghĩa Endpoint Interfaces ---
@route("/books")
interface Books {
  @get
  @summary("Lấy danh sách hệ thống sách")
  list(@query status?: BookStatus): Book[];

  @post
  @summary("Tạo mới một cuốn sách")
  create(@body body: BookInput): {
    @statusCode code: 201;
    @body book: Book;
  };

  @get
  @route("/{id}")
  @summary("Gọixem chi tiết sách")
  read(@path id: int32): Book | { @statusCode code: 404, @body error: ErrorResponse };
}

@route("/users")
interface Users {
  @get
  @summary("Lấy danh sách người dùng thư viện")
  list(): User[];

  @post
  @summary("Thêm hồ sơ người dùng mới")
  create(@body body: UserInput): {
    @statusCode code: 201;
    @body user: User;
  };
}
