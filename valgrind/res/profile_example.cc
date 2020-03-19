#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <map>

class DataBaseA {
 public:
  typedef std::pair<std::string, std::string> StringPair;

  void insert(const std::string &name, const std::string &food) {
    // only add new value if there is no value with that name.
    if (lookup(name).empty()) {
      data_.push_back({name, food});
    }
  }

  std::string lookup(const std::string &name) {
    // go through list and return value if it name exists
    for (const StringPair &value : data_) {
      if (value.first == name) {
        return value.second;
      }
    }
    // else return empty string
    return {};
  }

 private:
  std::vector<StringPair> data_;

};

class DataBaseB {
 public:

  void insert(const std::string &name, const std::string &food) {
    // only insert if there is no entry with the same name
    if (lookup(name).empty()) {
      data_[name] = food;
    }
  }

  std::string lookup(const std::string &name) {

    // if name is not found, return empty string
    if (data_.find(name) == data_.end()) {
      return {};
    } else {
      //otherwise return value
      return data_[name];
    }

  }

  std::map<std::string, std::string> data_;
};

int main(int argc, char *argv[]) {
  std::cout << "Simple profiling example!" << std::endl;
  /*
   * What does this program do?
   *  Let's assume we want to store the favourite food of many people.
   *  We use the persons name as an string index.
   *  There can only be one person with a specific name.
   *
   *  There are two implementations, A and B.
   *  A is a naive implementation using a vector with string/string pairs.
   *
   *  B uses the map provided by the standard library.
   *
   *
   */

  // set up both implementations
  DataBaseA data_a;
  DataBaseB data_b;

  // add a specific amount of people.
  // In this example, people are just named "Hans" + numbers,
  // and their favourite dish is always beer.

  // feel free to adjust the number of people to see relative scaling
  int num_people = 2500;

  for (int i = 0; i < num_people; ++i) {
    std::ostringstream name;
    name << "Hans" << i;

    data_a.insert(name.str(), "beer");
    data_b.insert(name.str(), "beer");
  }

  // we want to lookup the approx middle Hans, so we just integer divide:
  int middle = num_people / 2;

  std::ostringstream name;
  name << "Hans" << middle;

  std::cout << name.str() << ": " << data_a.lookup(name.str()) << std::endl;
  std::cout << name.str() << ": " << data_b.lookup(name.str()) << std::endl;

  return 0;

}