#include <casadi/core/xml_node.hpp>

int main(){

  auto X = casadi::XmlNode();
  X.set_attribute("Tiny", "XML");

  return 0;
}
