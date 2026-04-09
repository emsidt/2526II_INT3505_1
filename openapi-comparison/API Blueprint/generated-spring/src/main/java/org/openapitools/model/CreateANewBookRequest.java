package org.openapitools.model;

import java.net.URI;
import java.util.Objects;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonTypeName;
import java.math.BigDecimal;
import org.springframework.lang.Nullable;
import org.openapitools.jackson.nullable.JsonNullable;
import java.time.OffsetDateTime;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import io.swagger.v3.oas.annotations.media.Schema;


import java.util.*;
import jakarta.annotation.Generated;

/**
 * CreateANewBookRequest
 */

@JsonTypeName("Create_a_new_book_request")
@Generated(value = "org.openapitools.codegen.languages.SpringCodegen", date = "2026-04-03T08:59:41.342205400+07:00[Asia/Saigon]", comments = "Generator version: 7.21.0")
public class CreateANewBookRequest {

  private @Nullable String title;

  private @Nullable String author;

  private @Nullable BigDecimal publishedYear;

  public CreateANewBookRequest title(@Nullable String title) {
    this.title = title;
    return this;
  }

  /**
   * Get title
   * @return title
   */
  
  @Schema(name = "title", requiredMode = Schema.RequiredMode.NOT_REQUIRED)
  @JsonProperty("title")
  public @Nullable String getTitle() {
    return title;
  }

  @JsonProperty("title")
  public void setTitle(@Nullable String title) {
    this.title = title;
  }

  public CreateANewBookRequest author(@Nullable String author) {
    this.author = author;
    return this;
  }

  /**
   * Get author
   * @return author
   */
  
  @Schema(name = "author", requiredMode = Schema.RequiredMode.NOT_REQUIRED)
  @JsonProperty("author")
  public @Nullable String getAuthor() {
    return author;
  }

  @JsonProperty("author")
  public void setAuthor(@Nullable String author) {
    this.author = author;
  }

  public CreateANewBookRequest publishedYear(@Nullable BigDecimal publishedYear) {
    this.publishedYear = publishedYear;
    return this;
  }

  /**
   * Get publishedYear
   * @return publishedYear
   */
  @Valid 
  @Schema(name = "published_year", requiredMode = Schema.RequiredMode.NOT_REQUIRED)
  @JsonProperty("published_year")
  public @Nullable BigDecimal getPublishedYear() {
    return publishedYear;
  }

  @JsonProperty("published_year")
  public void setPublishedYear(@Nullable BigDecimal publishedYear) {
    this.publishedYear = publishedYear;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    CreateANewBookRequest createANewBookRequest = (CreateANewBookRequest) o;
    return Objects.equals(this.title, createANewBookRequest.title) &&
        Objects.equals(this.author, createANewBookRequest.author) &&
        Objects.equals(this.publishedYear, createANewBookRequest.publishedYear);
  }

  @Override
  public int hashCode() {
    return Objects.hash(title, author, publishedYear);
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class CreateANewBookRequest {\n");
    sb.append("    title: ").append(toIndentedString(title)).append("\n");
    sb.append("    author: ").append(toIndentedString(author)).append("\n");
    sb.append("    publishedYear: ").append(toIndentedString(publishedYear)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private String toIndentedString(@Nullable Object o) {
    return o == null ? "null" : o.toString().replace("\n", "\n    ");
  }
}

